"""Compare saved audits and measure small, paired fit-time experiments."""

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.tree import export_text
from threadpoolctl import threadpool_info, threadpool_limits

from inf8239_u04.data import features, load_data, temporal_split
from inf8239_u04.model import build_model


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def compare(root, repeats):
    out = root / "reports/lab12/comparison"
    out.mkdir(parents=True, exist_ok=True)
    kinds = ["logistic", "tree"]
    train, test = temporal_split(load_data())
    x_train, x_test = features(train), features(test)
    canonical = {kind: joblib.load(root / f"models/{kind}.joblib") for kind in kinds}
    predictions = {}
    metadata = {}
    summary_rows = []
    audit_frames = []
    for kind in kinds:
        base = root / f"reports/lab12/{kind}"
        saved = pd.read_csv(base / "test_predictions.csv")
        assert saved.case_id.tolist() == test.case_id.tolist()
        np.testing.assert_array_equal(saved.target, test.target)
        predictions[kind] = canonical[kind].predict(x_test)
        np.testing.assert_array_equal(saved.prediction, predictions[kind])
        metadata[kind] = json.loads((base / "model_metadata.json").read_text(encoding="utf-8"))
        assert digest(root / f"models/{kind}.joblib") == metadata[kind]["model_sha256"]
        assert metadata[kind]["train_n"] == len(train) and metadata[kind]["test_n"] == len(test)
        assert metadata[kind]["features"] == list(x_train.columns)
        assert metadata[kind]["dataset_sha256"] == digest(root / "data/territorial_risk_synthetic.csv")
        primary = json.loads((base / "global_metrics.json").read_text(encoding="utf-8"))
        frame = pd.read_csv(base / "audit_support.csv")
        frame.insert(0, "model", kind)
        audit_frames.append(frame)
        global_row = frame.loc[frame.level.eq("global")].iloc[0]
        gaps = json.loads((base / "gap_analysis.json").read_text(encoding="utf-8"))
        row = {"model": kind}
        for metric in ["accuracy", "recall", "fpr", "selection_rate", "precision", "f1", "fnr", "tp", "tn", "fp", "fn"]:
            value = global_row[metric]
            row[metric] = int(value) if metric in {"tp", "tn", "fp", "fn"} else float(value)
        for level in ["group", "intersection"]:
            for metric in ["recall", "fpr", "selection_rate"]:
                row[f"{level}_{metric}_gap"] = gaps[level][metric]["max_minus_min"]
        row["original_fit_seconds"] = primary["resources"]["training_seconds"]
        row["model_bytes"] = (root / f"models/{kind}.joblib").stat().st_size
        assert row["model_bytes"] / 1024 == primary["resources"]["model_kb"]
        summary_rows.append(row)
    assert metadata["logistic"]["packages"] == metadata["tree"]["packages"]
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(out / "model_comparison.csv", index=False)
    combined = pd.concat(audit_frames, ignore_index=True)
    combined.to_csv(out / "group_and_intersection_comparison.csv", index=False)
    for level in ["group", "intersection"]:
        left = combined.loc[(combined.model.eq("logistic")) & combined.level.eq(level)].set_index("group")
        right = combined.loc[(combined.model.eq("tree")) & combined.level.eq(level)].set_index("group")
        pd.testing.assert_frame_equal(left[["count", "positive_n", "negative_n"]], right[["count", "positive_n", "negative_n"]])
    discordance = pd.crosstab(predictions["logistic"] == test.target, predictions["tree"] == test.target)
    pairs = test[["case_id", "target", "protected_group", "age_band"]].copy()
    pairs["logistic_prediction"] = predictions["logistic"]
    pairs["tree_prediction"] = predictions["tree"]
    pairs["prediction_changed"] = predictions["logistic"] != predictions["tree"]
    pairs.to_csv(out / "paired_predictions.csv", index=False)

    # Fresh pipelines, one warm-up per model, then balanced alternating order.
    # Timer covers fit only; construction, prediction and serialization are excluded.
    measurements = []
    started = datetime.now(UTC).isoformat()
    with threadpool_limits(limits=1):
        for kind in kinds:
            build_model(kind).fit(x_train, train.target)
        pools = [{key: entry.get(key) for key in ["user_api", "internal_api", "num_threads", "prefix", "version"]} for entry in threadpool_info()]
        for repeat in range(repeats):
            order = kinds if repeat % 2 == 0 else list(reversed(kinds))
            for position, kind in enumerate(order):
                fitted = build_model(kind)
                tick = time.perf_counter()
                fitted.fit(x_train, train.target)
                seconds = time.perf_counter() - tick
                np.testing.assert_array_equal(fitted.predict(x_test), predictions[kind])
                measurements.append({"repeat": repeat + 1, "position": position + 1, "model": kind, "fit_seconds": seconds})
    timing = pd.DataFrame(measurements)
    timing.to_csv(out / "fit_benchmark_trials.csv", index=False)
    timing_summary = []
    for kind, group in timing.groupby("model", sort=True):
        values = group.fit_seconds.to_numpy()
        timing_summary.append({
            "model": kind, "repeats": len(values), "median_seconds": float(np.median(values)),
            "q25_seconds": float(np.quantile(values, 0.25)), "q75_seconds": float(np.quantile(values, 0.75)),
            "min_seconds": float(values.min()), "max_seconds": float(values.max()),
        })
    pd.DataFrame(timing_summary).to_csv(out / "fit_benchmark_summary.csv", index=False)
    benchmark = {
        "started_at_utc": started, "warmup_fits_per_model": 1,
        "measured_fits_per_model": repeats, "total_fit_calls": 2 + repeats * 2,
        "order": "alternating logistic/tree and tree/logistic",
        "timer": "time.perf_counter around pipeline.fit only",
        "controlled_native_thread_limit": 1, "observed_threadpools": pools,
        "same_train_test_ids_and_predictors": True,
        "all_trial_predictions_match_canonical_models": True,
        "canonical_models_overwritten": False,
        "machine": {"platform": platform.platform(), "processor": platform.processor(), "logical_cpu_count": os.cpu_count()},
        "python": sys.version,
        "packages": {name: importlib.metadata.version(name) for name in ["numpy", "pandas", "scikit-learn", "threadpoolctl"]},
        "summary": timing_summary,
        "energy_measured": False, "carbon_measured": False, "peak_ram_measured": False,
        "limitation": "Small local paired benchmark; timing does not measure energy, emissions, total lifecycle cost or universal model speed.",
    }
    write_json(out / "fit_benchmark_metadata.json", benchmark)

    logistic, tree = canonical["logistic"], canonical["tree"]
    feature_names = logistic[0].get_feature_names_out().tolist()
    pd.DataFrame({"feature": feature_names, "coefficient_log_odds": logistic[-1].coef_[0]}).to_csv(out / "logistic_coefficients.csv", index=False)
    tree_names = tree[0].get_feature_names_out().tolist()
    pd.DataFrame({"feature": tree_names, "impurity_based_importance": tree[-1].feature_importances_}).to_csv(out / "tree_feature_importances.csv", index=False)
    rules = "Numeric num__ features are standardized; cat__ features are one-hot indicators.\nThese rules are predictive associations on synthetic data, not causal explanations.\n\n"
    rules += export_text(tree[-1], feature_names=tree_names, max_depth=5, decimals=4)
    (out / "tree_rules.txt").write_text(rules, encoding="utf-8")
    tree_state = tree[-1].tree_.__getstate__()
    complexity = {
        "raw_features": len(x_train.columns), "transformed_features": len(feature_names), "train_rows": len(train),
        "logistic": {"coefficient_count": int(logistic[-1].coef_.size), "intercept_count": int(logistic[-1].intercept_.size), "iterations": logistic[-1].n_iter_.tolist(), "learned_array_buffer_bytes": int(logistic[-1].coef_.nbytes + logistic[-1].intercept_.nbytes)},
        "tree": {"depth": int(tree[-1].get_depth()), "nodes": int(tree[-1].tree_.node_count), "leaves": int(tree[-1].get_n_leaves()), "learned_array_buffer_bytes": int(tree_state["nodes"].nbytes + tree_state["values"].nbytes)},
        "buffer_scope": "Estimator coefficient or node/value arrays only; not total RAM or peak training memory.",
        "paired_test": {
            "same_predictions": int((~pairs.prediction_changed).sum()), "different_predictions": int(pairs.prediction_changed.sum()),
            "both_correct": int(discordance.loc[True, True]), "only_logistic_correct": int(discordance.loc[True, False]),
            "only_tree_correct": int(discordance.loc[False, True]), "both_wrong": int(discordance.loc[False, False]),
        },
    }
    write_json(out / "complexity_and_interpretability.json", complexity)
    print(summary.to_string(index=False))
    print(json.dumps({"benchmark": timing_summary, "complexity": complexity}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=10)
    args = parser.parse_args()
    if args.repeats < 2 or args.repeats % 2:
        parser.error("Use an even repeat count >=2 to balance model order")
    compare(Path.cwd(), args.repeats)


if __name__ == "__main__":
    main()

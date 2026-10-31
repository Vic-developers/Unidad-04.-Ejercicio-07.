"""Profile the synthetic dataset and explain existing audit outputs without refitting."""

import argparse
import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.stats import binomtest

from inf8239_u04.data import features, load_data, temporal_split
from inf8239_u04.fairness import intersectional


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def counts(series):
    return {str(key): int(value) for key, value in series.value_counts().sort_index().items()}


def profile(root):
    path = root / "data/territorial_risk_synthetic.csv"
    original_hash = digest(path)
    raw = pd.read_csv(path)
    df = load_data(path)
    train, test = temporal_split(df)
    numeric = ["previous_incidents", "infrastructure_score", "exposure"]
    predictor_columns = list(features(df).columns)
    excluded = ["case_id", "received_date", "protected_group", "target"]
    assert not set(excluded) & set(predictor_columns)
    assert set(train.case_id).isdisjoint(test.case_id)
    assert train.received_date.max() < test.received_date.min()
    assert df.case_id.is_unique and not df.isna().any().any()
    assert np.isfinite(df[numeric].to_numpy()).all()
    assert set(df.target) == {0, 1}
    profile_data = {
        "synthetic_only": True, "dataset_sha256": original_hash,
        "rows": len(df), "column_count": len(df.columns),
        "dtypes": {key: str(value) for key, value in df.dtypes.items()},
        "missing_counts": {key: int(value) for key, value in df.isna().sum().items()},
        "duplicate_ids": int(df.case_id.duplicated().sum()),
        "duplicate_full_rows": int(raw.duplicated().sum()),
        "duplicate_predictor_rows": int(features(df).duplicated().sum()),
        "numeric_values_finite": True,
        "previous_incidents_nonnegative_integer": bool(
            df.previous_incidents.ge(0).all() and df.previous_incidents.mod(1).eq(0).all()
        ),
        "numeric_summary": df[numeric].describe().to_dict(),
        "categories": {column: counts(df[column]) for column in ["zone", "protected_group", "age_band"]},
        "raw_dates_already_sorted": bool(pd.to_datetime(raw.received_date).is_monotonic_increasing),
        "unique_dates": int(df.received_date.nunique()),
        "predictors": predictor_columns, "excluded_from_predictors": excluded,
        "split": {},
        "test_categories_absent_from_training": {
            column: sorted(set(test[column]) - set(train[column]))
            for column in ["zone", "age_band"]
        },
        "cross_split_duplicate_predictor_rows": len(
            set(features(train).itertuples(index=False, name=None))
            & set(features(test).itertuples(index=False, name=None))
        ),
        "limitation": "Observed quality checks do not establish label validity, pre-event availability or validity for real populations.",
    }
    split_frames = []
    for label, subset in [("all", df), ("train", train), ("test", test)]:
        profile_data["split"][label] = {
            "n": len(subset), "start": str(subset.received_date.min().date()),
            "end": str(subset.received_date.max().date()), "target": counts(subset.target),
            "protected_group": counts(subset.protected_group),
            "group_target": subset.groupby(["protected_group", "target"]).size().unstack(fill_value=0).to_dict(orient="index"),
        }
        if label != "all":
            item = subset[["case_id", "received_date", "protected_group", "age_band", "target"]].copy()
            item["split"] = label
            split_frames.append(item)
    # JSON keys for target class counts are strings after serialization.
    out = root / "reports/lab12"
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "dataset_profile.json", profile_data)
    pd.concat(split_frames).to_csv(out / "temporal_split.csv", index=False)
    assert digest(path) == original_hash
    print(json.dumps({"rows": len(df), "predictors": predictor_columns, "split": profile_data["split"]}, ensure_ascii=False))
    return df, train, test


def ratio(numerator, denominator):
    return float(numerator / denominator) if denominator else None


def summarize(subset, level, group):
    y, prediction = subset.target.to_numpy(), subset.prediction.to_numpy()
    tp = int(((y == 1) & (prediction == 1)).sum())
    tn = int(((y == 0) & (prediction == 0)).sum())
    fp = int(((y == 0) & (prediction == 1)).sum())
    fn = int(((y == 1) & (prediction == 0)).sum())
    n = len(subset)
    positive, negative, selected = tp + fn, tn + fp, tp + fp
    row = {
        "level": level, "group": group, "count": n,
        "positive_n": positive, "negative_n": negative, "selected_n": selected,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "prevalence": ratio(positive, n), "accuracy": ratio(tp + tn, n),
        "recall": ratio(tp, positive), "fpr": ratio(fp, negative),
        "fnr": ratio(fn, positive), "selection_rate": ratio(selected, n),
        "precision": ratio(tp, selected), "f1": ratio(2 * tp, 2 * tp + fp + fn),
        "small_total_n_lt30": n < 30,
        "small_positive_n_lt10": positive < 10,
        "small_negative_n_lt10": negative < 10,
    }
    for metric, numerator, denominator in [
        ("recall", tp, positive), ("fpr", fp, negative), ("selection_rate", selected, n)
    ]:
        low = high = None
        if denominator:
            interval = binomtest(numerator, denominator).proportion_ci(confidence_level=0.95, method="wilson")
            low, high = float(interval.low), float(interval.high)
        row[f"{metric}_wilson95_low"] = low
        row[f"{metric}_wilson95_high"] = high
    return row


def audit_support(root, train, test, kind):
    model_path = root / f"models/{kind}.joblib"
    out = root / f"reports/lab12/{kind}"
    # Only load the model just produced locally by the supplied audit command.
    model = joblib.load(model_path)
    assert list(model.feature_names_in_) == list(features(train).columns)
    assert model[-1].random_state == 42
    prep = model[0]
    numeric = ["previous_incidents", "infrastructure_score", "exposure"]
    scaler = prep.named_transformers_["num"]
    np.testing.assert_allclose(scaler.mean_, train[numeric].mean().to_numpy(), rtol=0, atol=1e-12)
    assert int(scaler.n_samples_seen_) == len(train)
    encoder = prep.named_transformers_["cat"]
    for column, categories in zip(["zone", "age_band"], encoder.categories_, strict=True):
        assert set(categories) == set(train[column])
    output = test[["case_id", "received_date", "protected_group", "age_band", "target"]].copy()
    output["prediction"] = model.predict(features(test))
    output["probability_class_1"] = model.predict_proba(features(test))[:, list(model.classes_).index(1)]
    output["intersection"] = intersectional(test)
    output.to_csv(out / "test_predictions.csv", index=False)
    rows = [summarize(output, "global", "ALL")]
    for level, column in [("group", "protected_group"), ("intersection", "intersection")]:
        rows.extend(summarize(subset, level, str(group)) for group, subset in output.groupby(column, sort=True))
    details = pd.DataFrame(rows)
    details.to_csv(out / "audit_support.csv", index=False)

    primary = json.loads((out / "global_metrics.json").read_text(encoding="utf-8"))
    standard_metrics = ["count", "accuracy", "selection_rate", "recall", "precision", "fpr"]
    for metric in standard_metrics:
        np.testing.assert_allclose(rows[0][metric], primary["metrics"][metric], atol=1e-12, rtol=0)
    for level, filename in [("group", "fairness_by_group.csv"), ("intersection", "fairness_intersectional.csv")]:
        saved = pd.read_csv(out / filename, index_col=0)
        calculated = details.loc[details.level.eq(level)].set_index("group")
        assert set(saved.index) == set(calculated.index)
        np.testing.assert_allclose(
            saved[standard_metrics].sort_index(), calculated[standard_metrics].sort_index(), rtol=0, atol=1e-12
        )
    gaps = {}
    for level in ["group", "intersection"]:
        frame = details.loc[details.level.eq(level)].set_index("group")
        gaps[level] = {}
        for metric in ["accuracy", "recall", "fpr", "selection_rate", "precision", "fnr"]:
            values = frame[metric].dropna()
            gaps[level][metric] = {
                "max_minus_min": float(values.max() - values.min()),
                "min_group": str(values.idxmin()), "max_group": str(values.idxmax()),
            }
            if level == "group":
                gaps[level][metric]["G2_minus_G1"] = float(values.loc["G2"] - values.loc["G1"])
                if metric in primary["differences"]:
                    np.testing.assert_allclose(values.max() - values.min(), primary["differences"][metric], atol=1e-12, rtol=0)
    write_json(out / "gap_analysis.json", gaps)
    metadata = {
        "kind": kind, "model_sha256": digest(model_path), "model_bytes": model_path.stat().st_size,
        "dataset_sha256": digest(root / "data/territorial_risk_synthetic.csv"),
        "python": sys.version,
        "packages": {name: importlib.metadata.version(name) for name in ["scikit-learn", "fairlearn", "pandas", "numpy", "scipy", "joblib"]},
        "features": list(model.feature_names_in_), "transformed_feature_count": int(model[-1].n_features_in_),
        "estimator_parameters": {name: model[-1].get_params()[name] for name in ["class_weight", "random_state", "max_iter", "solver", "C", "tol"]},
        "iterations": model[-1].n_iter_.tolist(),
        "train_n": len(train), "test_n": len(test),
        "fitted_scaler_matches_training_only": True,
        "encoder_categories_match_training_only": True,
        "primary_metrics_match_reconstructed_counts": True,
        "refitted_by_support_script": False,
        "interval_method": "SciPy binomtest.proportion_ci: Wilson 95%, no continuity correction",
        "support_flags": "Descriptive warnings only: n<30, positive_n<10 or negative_n<10; not fairness acceptance thresholds.",
        "uncertainty_limitations": "Conditional binomial intervals; no model-training uncertainty, simultaneous gap inference or external population validity established.",
    }
    write_json(out / "model_metadata.json", metadata)
    print(details[["level", "group", "count", "positive_n", "negative_n", "tp", "tn", "fp", "fn", "recall", "fpr"]].to_string(index=False))
    print(json.dumps({"verified_primary_metrics": True, "model_sha256": metadata["model_sha256"], "gaps": gaps}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-only", action="store_true")
    parser.add_argument("--model", choices=["logistic"], default="logistic")
    args = parser.parse_args()
    root = Path.cwd()
    _, train, test = profile(root)
    if not args.profile_only:
        audit_support(root, train, test, args.model)


if __name__ == "__main__":
    main()

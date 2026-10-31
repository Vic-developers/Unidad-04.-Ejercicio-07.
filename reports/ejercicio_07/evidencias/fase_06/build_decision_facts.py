"""Reconstruct decision facts from saved predictions without loading or fitting models."""

import csv
import hashlib
import json
import math
from pathlib import Path

import yaml


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def measure(records):
    counts = {key: 0 for key in ("tp", "tn", "fp", "fn")}
    for row in records:
        truth, predicted = int(row["target"]), int(row["prediction"])
        assert truth in (0, 1) and predicted in (0, 1)
        key = {(1, 1): "tp", (0, 0): "tn", (0, 1): "fp", (1, 0): "fn"}[(truth, predicted)]
        counts[key] += 1
    tp, tn, fp, fn = (counts[key] for key in ("tp", "tn", "fp", "fn"))
    return {
        "n": len(records), "positive_n": tp + fn, "negative_n": tn + fp,
        "selected_n": tp + fp, **counts,
        "accuracy": (tp + tn) / len(records), "recall": tp / (tp + fn),
        "fpr": fp / (fp + tn), "selection_rate": (tp + fp) / len(records),
        "fnr": fn / (tp + fn), "precision": tp / (tp + fp),
        "f1": 2 * tp / (2 * tp + fp + fn),
    }


def main():
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    input_paths = {
        "data/territorial_risk_synthetic.csv", "student_inputs/risk_register.csv",
        "configs/governance.yml", "reports/lab12/comparison/model_comparison.csv",
        "reports/lab12/comparison/fit_benchmark_summary.csv",
        "reports/lab12/comparison/complexity_and_interpretability.json",
        "reports/ejercicio_07/evidencias/fase_05/legal_context.json",
    }
    comparison = {row["model"]: row for row in rows(root / "reports/lab12/comparison/model_comparison.csv")}
    benchmark = {row["model"]: row for row in rows(root / "reports/lab12/comparison/fit_benchmark_summary.csv")}
    models = {}
    predictions = {}
    for name in ("logistic", "tree"):
        folder = f"reports/lab12/{name}"
        input_paths.update(f"{folder}/{filename}" for filename in ("test_predictions.csv", "global_metrics.json", "gap_analysis.json", "model_metadata.json"))
        records = rows(root / folder / "test_predictions.csv")
        predictions[name] = {row["case_id"]: row for row in records}
        assert len(records) == len(predictions[name]) == 160
        global_metrics = measure(records)
        saved = load(root / folder / "global_metrics.json")
        metadata = load(root / folder / "model_metadata.json")
        for key, value in saved["metrics"].items():
            actual = global_metrics["n"] if key == "count" else global_metrics[key]
            assert math.isclose(actual, value, rel_tol=1e-12, abs_tol=1e-12), (name, key)
        for key in ("accuracy", "recall", "fpr", "selection_rate", "precision", "f1", "fnr", "tp", "tn", "fp", "fn"):
            assert math.isclose(global_metrics[key], float(comparison[name][key]), rel_tol=1e-12, abs_tol=1e-12)
        groups = {}
        for column, label in (("protected_group", "group"), ("intersection", "intersection")):
            groups[label] = {group: measure([row for row in records if row[column] == group]) for group in sorted({row[column] for row in records})}
        gaps = {}
        saved_gaps = load(root / folder / "gap_analysis.json")
        for label, strata in groups.items():
            gaps[label] = {}
            for metric in ("recall", "fpr", "selection_rate"):
                gap = max(item[metric] for item in strata.values()) - min(item[metric] for item in strata.values())
                assert math.isclose(gap, saved_gaps[label][metric]["max_minus_min"], abs_tol=1e-12)
                assert math.isclose(gap, float(comparison[name][f"{label}_{metric}_gap"]), abs_tol=1e-12)
                gaps[label][metric] = gap
        model_path = root / "models" / f"{name}.joblib"
        assert digest(model_path) == metadata["model_sha256"]
        assert model_path.stat().st_size == metadata["model_bytes"] == int(comparison[name]["model_bytes"])
        supports = [item["n"] for item in groups["intersection"].values()]
        models[name] = {
            "global": global_metrics, "by_group": groups["group"], "by_intersection": groups["intersection"],
            "gaps": gaps, "intersection_count": len(supports), "intersections_with_n_lt30": sum(n < 30 for n in supports),
            "intersection_n_min": min(supports), "intersection_n_max": max(supports),
            "model_bytes": metadata["model_bytes"], "model_sha256": metadata["model_sha256"],
            "features": metadata["features"],
            "fit_benchmark_existing": {key: int(value) if key == "repeats" else float(value) for key, value in benchmark[name].items() if key != "model"},
        }

    left, right = predictions["logistic"], predictions["tree"]
    assert left.keys() == right.keys()
    paired = {key: 0 for key in ("same_predictions", "different_predictions", "both_correct", "only_logistic_correct", "only_tree_correct", "both_wrong")}
    for case_id, row in left.items():
        other = right[case_id]
        assert all(row[key] == other[key] for key in ("target", "received_date", "protected_group", "age_band"))
        paired["same_predictions" if row["prediction"] == other["prediction"] else "different_predictions"] += 1
        correct_left = row["prediction"] == row["target"]
        correct_right = other["prediction"] == other["target"]
        outcome = {(True, True): "both_correct", (True, False): "only_logistic_correct", (False, True): "only_tree_correct", (False, False): "both_wrong"}[(correct_left, correct_right)]
        paired[outcome] += 1
    complexity = load(root / "reports/lab12/comparison/complexity_and_interpretability.json")
    assert paired == complexity["paired_test"]
    dataset = rows(root / "data/territorial_risk_synthetic.csv")
    assert len(dataset) == 640
    context = load(root / "reports/ejercicio_07/evidencias/fase_05/legal_context.json")
    result = {
        "scope": "Reconstruction from saved outputs; no model fit, new predictions, mitigation experiment or human approval.",
        "dataset": {"n": len(dataset), "train_n": 480, "test_n": 160, "synthetic_scope": "documented_by_project_not_independently_verified", "sha256": digest(root / "data/territorial_risk_synthetic.csv")},
        "jurisdiction": context["jurisdiction"], "models": models, "paired_test": paired,
        "complexity_existing": complexity,
        "experimental_gates_not_approved": yaml.safe_load((root / "configs/governance.yml").read_text(encoding="utf-8"))["gates"],
        "risk_baselines": [{key: row[key] for key in ("id", "likelihood_1_4", "impact_1_4", "owner", "residual")} for row in rows(root / "student_inputs/risk_register.csv")],
        "risk_acceptance": "pending_user_approval", "test_already_inspected": True,
        "new_model_fits": 0, "new_predictions": 0, "mitigation_effect_measured": False,
        "source_files": [{"path": relative, "sha256": digest(root / relative)} for relative in sorted(input_paths)],
    }
    (evidence / "decision_facts.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"saved_models_checked": list(models), "test_n": len(left), "risk_baselines": len(result["risk_baselines"]), "sources": len(input_paths), "new_model_fits": 0, "new_predictions": 0, "mitigation_effect_measured": False}))


if __name__ == "__main__":
    main()

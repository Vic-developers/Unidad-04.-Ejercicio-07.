"""Verify the comparison and preserve previous evidence without fitting models."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    initial = json.loads((evidence / "initial_state.json").read_text(encoding="utf-8"))
    changed = []
    for item in initial["files"]:
        path = root / item["path"]
        assert path.is_file(), item["path"]
        if digest(path) != item["sha256"]:
            changed.append(item["path"])
    allowed = ["scripts/lab12_supporting_evidence.py", "tests/test_fairness.py", "tests/test_model.py"]
    assert sorted(changed) == allowed, changed
    for label in ["01_tree_audit", "03_tree_support_final", "04_comparison_and_benchmark", "05_code_style", "06_both_models_tests", "07_style_final"]:
        record = json.loads((evidence / f"{label}.json").read_text(encoding="utf-8"))
        assert record["exit_code"] == 0, label
    failed = json.loads((evidence / "02_tree_support.json").read_text(encoding="utf-8"))
    assert failed["exit_code"] == 1 and "int64 is not JSON serializable" in failed["stderr"]
    test_log = json.loads((evidence / "06_both_models_tests.json").read_text(encoding="utf-8"))
    assert "4 passed" in test_log["stdout"]
    comparison = root / "reports/lab12/comparison"
    table = pd.read_csv(comparison / "model_comparison.csv").set_index("model")
    paired = pd.read_csv(comparison / "paired_predictions.csv")
    split = pd.read_csv(root / "reports/lab12/temporal_split.csv")
    assert len(paired) == 160 and paired.case_id.is_unique
    assert set(paired.case_id) == set(split.loc[split.split.eq("test"), "case_id"])
    for kind in ["logistic", "tree"]:
        base = root / f"reports/lab12/{kind}"
        primary = json.loads((base / "global_metrics.json").read_text(encoding="utf-8"))
        metadata = json.loads((base / "model_metadata.json").read_text(encoding="utf-8"))
        model_path = root / f"models/{kind}.joblib"
        assert digest(model_path) == metadata["model_sha256"]
        assert model_path.stat().st_size == int(table.loc[kind, "model_bytes"])
        assert metadata["train_n"] == 480 and metadata["test_n"] == 160
        assert "protected_group" not in metadata["features"]
        for metric in ["accuracy", "recall", "fpr", "selection_rate", "precision"]:
            np.testing.assert_allclose(table.loc[kind, metric], primary["metrics"][metric], rtol=0, atol=1e-12)
        predictions = pd.read_csv(base / "test_predictions.csv")
        assert predictions.case_id.tolist() == paired.case_id.tolist()
        np.testing.assert_array_equal(predictions.prediction, paired[f"{kind}_prediction"])
        frame = pd.read_csv(base / "audit_support.csv")
        assert len(frame.loc[frame.level.eq("intersection")]) == 8
    combined = pd.read_csv(comparison / "group_and_intersection_comparison.csv")
    for level in ["group", "intersection"]:
        a = combined.loc[(combined.model.eq("logistic")) & combined.level.eq(level)].set_index("group")
        b = combined.loc[(combined.model.eq("tree")) & combined.level.eq(level)].set_index("group")
        pd.testing.assert_frame_equal(a[["count", "positive_n", "negative_n"]], b[["count", "positive_n", "negative_n"]])
    trials = pd.read_csv(comparison / "fit_benchmark_trials.csv")
    benchmark = json.loads((comparison / "fit_benchmark_metadata.json").read_text(encoding="utf-8"))
    assert len(trials) == 20 and trials.fit_seconds.gt(0).all()
    assert set(trials.groupby(["model", "position"]).size()) == {5}
    assert benchmark["total_fit_calls"] == 22
    assert benchmark["all_trial_predictions_match_canonical_models"]
    assert not benchmark["canonical_models_overwritten"]
    assert all(pool["num_threads"] == 1 for pool in benchmark["observed_threadpools"])
    for item in benchmark["summary"]:
        values = trials.loc[trials.model.eq(item["model"]), "fit_seconds"]
        assert len(values) == item["repeats"] == 10
        np.testing.assert_allclose(values.median(), item["median_seconds"], rtol=0, atol=1e-12)
    assert not benchmark["energy_measured"] and not benchmark["carbon_measured"]
    structure = json.loads((comparison / "complexity_and_interpretability.json").read_text(encoding="utf-8"))
    assert structure["tree"] == {"depth": 5, "nodes": 51, "leaves": 26, "learned_array_buffer_bytes": 4080}
    assert structure["paired_test"]["different_predictions"] == int(paired.prediction_changed.sum()) == 30
    assert sum(structure["paired_test"][key] for key in ["both_correct", "only_logistic_correct", "only_tree_correct", "both_wrong"]) == 160
    assert (root / "reports/ejercicio_07/COMPARACION_MODELOS.md").is_file()
    result = {
        "status": "passed", "starting_commit": initial["starting_commit"],
        "previous_files_checked": len(initial["files"]), "authorized_changed_files": changed,
        "previous_logistic_model_and_outputs_preserved": True,
        "dataset_lock_LAB11_and_decision_yaml_preserved": True,
        "same_test_ids_and_support": True, "test_cases": 160, "required_tests_passed": 4,
        "benchmark_trials": len(trials), "balanced_model_order": True,
        "benchmark_models_not_saved_over_canonical_models": True,
        "both_model_hashes_match_metadata": True, "metadata_export_failure_preserved_and_corrected": True,
        "energy_and_carbon_not_measured": True, "human_approval": "pending",
    }
    (evidence / "integrity_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

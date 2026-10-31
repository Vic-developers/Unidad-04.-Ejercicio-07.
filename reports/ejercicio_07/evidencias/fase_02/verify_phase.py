"""Check LAB12 evidence, provenance and phase boundaries without fitting a model."""

import hashlib
import json
from pathlib import Path

import pandas as pd
import yaml


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
    assert changed == ["student_inputs/lab12_decision.yml"], changed
    decision = yaml.safe_load((root / changed[0]).read_text(encoding="utf-8"))
    assert len(decision) == 6
    assert all(isinstance(value, str) and value.strip() and "REPLACE" not in value for value in decision.values())
    for relative in decision["evidence"].split(";"):
        assert (root / relative.strip()).is_file(), relative
    required_logs = [
        "01_dataset_profile", "02_logistic_audit", "03_support_and_uncertainty",
        "05_required_tests", "06_style_final", "07_final_support_verification",
        "08_decision_yaml_validation", "09_final_decision_validation",
    ]
    for label in required_logs:
        record = json.loads((evidence / f"{label}.json").read_text(encoding="utf-8"))
        assert record["exit_code"] == 0, label
    assert "2 passed" in json.loads((evidence / "05_required_tests.json").read_text(encoding="utf-8"))["stdout"]
    known_style_attempt = json.loads((evidence / "04_code_style.json").read_text(encoding="utf-8"))
    assert known_style_attempt["exit_code"] == 1
    out = root / "reports/lab12/logistic"
    predictions = pd.read_csv(out / "test_predictions.csv")
    split = pd.read_csv(root / "reports/lab12/temporal_split.csv")
    assert len(split) == 640 and split.case_id.is_unique
    test_ids = set(split.loc[split.split.eq("test"), "case_id"])
    assert len(predictions) == len(test_ids) == 160 and set(predictions.case_id) == test_ids
    assert set(predictions.prediction) <= {0, 1}
    support = pd.read_csv(out / "audit_support.csv")
    inter = support.loc[support.level.eq("intersection")]
    assert len(inter) == 8 and inter["count"].sum() == 160
    assert support.loc[support.level.eq("group"), "count"].sum() == 160
    assert inter["count"].min() == 8 and inter["count"].max() == 35
    assert int(inter.small_total_n_lt30.sum()) == 7
    assert inter.positive_n.min() == 4 and inter.negative_n.min() == 2
    for metric in ["recall", "fpr", "selection_rate"]:
        assert support[f"{metric}_wilson95_low"].ge(0).all()
        assert support[f"{metric}_wilson95_high"].le(1).all()
        assert support[f"{metric}_wilson95_low"].le(support[metric] + 1e-12).all()
        assert support[f"{metric}_wilson95_high"].ge(support[metric] - 1e-12).all()
    metadata = json.loads((out / "model_metadata.json").read_text(encoding="utf-8"))
    assert digest(root / "models/logistic.joblib") == metadata["model_sha256"]
    assert "protected_group" not in metadata["features"]
    assert metadata["fitted_scaler_matches_training_only"]
    assert not (root / "models/tree.joblib").exists()
    assert not (root / "reports/lab12/tree").exists()

    original = json.loads((root / "reports/ejercicio_07/evidencias/fase_00/diagnostico_estatico.json").read_text(encoding="utf-8"))
    original_source = Path(original["source_root"])
    source_status = "not_available_on_this_machine"
    if original_source.exists():
        assert len([path for path in original_source.rglob("*") if path.is_file()]) == 42
        for item in original["inventory"]:
            assert digest(original_source / item["path"]) == item["sha256"]
        source_status = "42_of_42_unchanged"
    result = {
        "status": "passed", "starting_commit": initial["starting_commit"],
        "previous_files_checked": len(initial["files"]), "authorized_changed_files": changed,
        "dataset_lock_LAB11_and_original_audit_unchanged": True,
        "original_source": source_status,
        "decision_fields_complete": len(decision), "decision_evidence_paths_exist": True,
        "required_tests_passed": 2, "initial_style_failure_preserved_and_corrected": True,
        "test_predictions": len(predictions), "intersections": len(inter),
        "intersections_n_lt30": int(inter.small_total_n_lt30.sum()),
        "intervals_contain_point_estimates": True,
        "saved_model_matches_metadata": True, "tree_not_executed": True,
        "human_approval": "pending",
    }
    (evidence / "integrity_verification.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

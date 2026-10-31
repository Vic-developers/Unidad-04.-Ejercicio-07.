"""Validate risk links, saved metrics and preservation of all prior phase files."""

import csv
import hashlib
import json
import math
import re
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def percentage(value):
    return str((Decimal(str(value)) * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def close(left, right):
    assert math.isclose(float(left), float(right), rel_tol=0, abs_tol=1e-12), (left, right)


def main():
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    initial = read_json(evidence / "initial_state.json")
    for item in initial["files"]:
        path = root / item["path"]
        assert path.is_file(), item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], item["path"]
    facts = read_json(evidence / "integration_facts.json")
    risk_rows = read_csv(root / "student_inputs/risk_register.csv")
    risks = {row["id"]: row for row in risk_rows}
    assert facts["lab11_risks"] == risk_rows
    matrix = read_csv(root / "reports/ejercicio_07/MATRIZ_TRAZABILIDAD.csv")
    assert len(matrix) == 9 and {row["risk_id"] for row in matrix} == set(risks)
    assert len({row["risk_id"] for row in matrix}) == len(matrix)
    links_checked = 0
    for row in matrix:
        original = risks[row["risk_id"]]
        assert all(value.strip() and "REPLACE" not in value for value in row.values())
        assert row["affected_group"] == original["affected"]
        assert row["proposed_owner"] == original["owner"]
        assert row["residual_lab11"] == row["residual_integrated_proposal"] == original["residual"]
        for field in ["lab11_evidence", "lab12_evidence"]:
            for relative in row[field].split(";"):
                target = (root / relative.strip()).resolve()
                assert target.is_relative_to(root.resolve()) and target.is_file(), relative
                links_checked += 1
    models = facts["models"]
    for kind, info in models.items():
        base = root / f"reports/lab12/{kind}"
        assert info["primary"] == read_json(base / "global_metrics.json")
        assert info["gaps"] == read_json(base / "gap_analysis.json")
        assert info["metadata"] == read_json(base / "model_metadata.json")
        predictions = read_csv(base / "test_predictions.csv")
        assert len(predictions) == 160
        for saved in info["support"]:
            if saved["level"] == "global":
                subset = predictions
            elif saved["level"] == "group":
                subset = [row for row in predictions if row["protected_group"] == saved["group"]]
            else:
                subset = [row for row in predictions if row["protected_group"] + " | " + row["age_band"] == saved["group"]]
            actual = {name: 0 for name in ["tp", "tn", "fp", "fn"]}
            for row in subset:
                pair = (int(row["target"]), int(row["prediction"]))
                actual[{(1, 1): "tp", (0, 0): "tn", (0, 1): "fp", (1, 0): "fn"}[pair]] += 1
            for name, value in actual.items():
                assert saved[name] == value
            tp, tn, fp, fn = (actual[name] for name in ["tp", "tn", "fp", "fn"])
            assert saved["count"] == len(subset)
            assert saved["positive_n"] == tp + fn and saved["negative_n"] == tn + fp
            close(saved["accuracy"], (tp + tn) / len(subset))
            close(saved["recall"], tp / (tp + fn))
            close(saved["fnr"], fn / (tp + fn))
            close(saved["fpr"], fp / (fp + tn))
            close(saved["selection_rate"], (tp + fp) / len(subset))
        for level in ["group", "intersection"]:
            rows = [row for row in info["support"] if row["level"] == level]
            for metric in ["recall", "fpr", "selection_rate"]:
                close(max(row[metric] for row in rows) - min(row[metric] for row in rows), info["gaps"][level][metric]["max_minus_min"])
    by_id = {row["risk_id"]: row for row in matrix}
    for kind in ["logistic", "tree"]:
        for metric in ["recall", "fpr"]:
            assert percentage(models[kind]["gaps"]["group"][metric]["max_minus_min"]) in by_id["R01"]["lab12_finding"]
    for kind in ["logistic", "tree"]:
        overall = next(row for row in models[kind]["support"] if row["level"] == "global")
        assert str(overall["fn"]) in by_id["R02"]["lab12_finding"]
        assert f"{overall['fp']}/{overall['negative_n']}" in by_id["R03"]["lab12_finding"]
    report = (root / "reports/ejercicio_07/EVALUACION_INTEGRADA.md").read_text(encoding="utf-8")
    assert set(re.findall(r"^\| (R\d{2}) ·", report, flags=re.MULTILINE)) == set(risks)
    assert set(re.findall(r"^\| (\d+)\. ", report, flags=re.MULTILINE)) == {str(number) for number in range(1, 11)}
    assert report.count("```") % 2 == 0
    assert "REVIEW" in report and "pendiente de aprobación" in report
    phase1 = read_json(root / "reports/ejercicio_07/evidencias/fase_01/execution_log.json")
    pytest1 = [item for item in phase1["commands"] if "pytest" in item["command"]]
    assert all(item["exit_code"] == 0 for item in pytest1)
    assert sum(int(re.search(r"(\d+) passed", item["stdout"])[1]) for item in pytest1) == 8
    for phase, filename, expected in [("02", "05_required_tests.json", 2), ("03", "06_both_models_tests.json", 4)]:
        record = read_json(root / f"reports/ejercicio_07/evidencias/fase_{phase}/{filename}")
        assert record["exit_code"] == 0 and f"{expected} passed" in record["stdout"]
    result = {
        "status": "passed", "starting_commit": initial["starting_commit"],
        "previous_files_unchanged": len(initial["files"]), "matrix_risks": len(matrix),
        "risk_coverage_complete": True, "evidence_path_references_checked": links_checked,
        "affected_groups_owners_residuals_match_LAB11": True,
        "independent_confusion_and_rate_reconstruction": True,
        "models_checked": list(models), "test_cases_per_model": 160,
        "integrated_questions_covered": 10, "previous_test_records_verified": {"phase_01": 8, "phase_02": 2, "phase_03": 4},
        "new_pytest_executions": 0, "new_model_fits": 0, "human_approval": "pending",
    }
    (evidence / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

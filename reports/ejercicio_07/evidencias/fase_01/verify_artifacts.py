"""Validate the real LAB11 inputs and outputs without training a model."""

import hashlib
import json
from pathlib import Path

import pandas as pd
import yaml


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root):
    evidence = root / "reports/ejercicio_07/evidencias/fase_01"
    baseline = json.loads(
        (root / "reports/ejercicio_07/evidencias/fase_00/diagnostico_estatico.json")
        .read_text(encoding="utf-8")
    )
    original = {entry["path"]: entry for entry in baseline["inventory"]}
    source = Path(baseline["source_root"])
    original_source_check = "unavailable_on_this_machine"
    if source.exists():
        source_files = sorted(p for p in source.rglob("*") if p.is_file())
        assert len(source_files) == len(original), "Original source file count changed"
        for relative, entry in original.items():
            assert sha256(source / relative) == entry["sha256"], relative
        original_source_check = "42_of_42_unchanged"

    impact = yaml.safe_load((root / "student_inputs/lab11_impact.yml").read_text(encoding="utf-8"))
    assert len(impact) == 9
    assert all(isinstance(value, str) and value.strip() and "REPLACE" not in value for value in impact.values())
    stakeholders = pd.read_csv(root / "student_inputs/stakeholders.csv")
    generated_stakeholders = pd.read_csv(root / "reports/lab11/stakeholders.csv")
    pd.testing.assert_frame_equal(stakeholders, generated_stakeholders)
    assert len(stakeholders) == 6
    assert not stakeholders.isna().any().any()

    risks = pd.read_csv(root / "student_inputs/risk_register.csv")
    scored = pd.read_csv(root / "reports/lab11/risk_register_scored.csv")
    assert len(risks) == len(scored) == 9
    assert risks.id.is_unique and set(risks.id) == set(scored.id)
    assert not risks.isna().any().any()
    assert not risks.astype(str).apply(lambda column: column.str.contains("REPLACE")).any().any()
    for column in ["likelihood_1_4", "impact_1_4"]:
        values = pd.to_numeric(risks[column])
        assert values.between(1, 4).all() and values.mod(1).eq(0).all()
    expected = risks.set_index("id")
    actual = scored.set_index("id")
    pd.testing.assert_frame_equal(
        expected.sort_index(), actual[risks.columns.drop("id")].sort_index()
    )
    assert actual.priority.sort_index().eq(
        (expected.likelihood_1_4 * expected.impact_1_4).sort_index()
    ).all()
    assert scored.priority.is_monotonic_decreasing
    assert set(risks.residual) <= {"low", "medium", "high"}
    assert set(risks.owner) <= set(stakeholders.stakeholder)

    summary = json.loads((root / "reports/lab11/rmf_summary.json").read_text(encoding="utf-8"))
    assert set(summary) == {"GOVERN", "MAP", "MEASURE", "MANAGE"}
    assert summary["MAP"]["risk_count"] == len(risks)
    assert summary["MAP"]["stakeholder_count"] == len(stakeholders)
    assert summary["MANAGE"]["deployment_authorized"] is False
    for section in summary.values():
        for relative in section.get("evidence", []):
            assert (root / relative).is_file(), relative
    assert (root / summary["MANAGE"]["traceability_document"]).is_file()

    assert sha256(root / "data/territorial_risk_synthetic.csv") == original["data/territorial_risk_synthetic.csv"]["sha256"]
    assert sha256(root / "uv.lock") == original["uv.lock"]["sha256"]
    assert sha256(root / "student_inputs/lab12_decision.yml") == original["student_inputs/lab12_decision.yml"]["sha256"]
    assert not list((root / "models").glob("*.joblib"))
    assert sorted(p.name for p in (root / "reports/lab12").iterdir()) == [".gitkeep"]
    result = {
        "status": "passed",
        "impact_fields_complete": len(impact),
        "stakeholders_complete_and_output_matches": len(stakeholders),
        "risks_complete_and_scores_verified": len(risks),
        "ordinal_values_in_range": True,
        "risk_owners_match_stakeholder_roles": True,
        "rmf_functions": sorted(summary),
        "dataset_unchanged": True,
        "uv_lock_unchanged": True,
        "original_source_integrity": original_source_check,
        "lab12_inputs_unchanged": True,
        "lab12_outputs_absent": True,
        "trained_model_files_absent": True,
        "priorities": scored[["id", "priority", "residual"]].to_dict(orient="records"),
        "limitation": "Checks validate structure and arithmetic, not empirical risk calibration or fairness.",
    }
    (evidence / "artifact_verification.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    verify(Path(__file__).resolve().parents[4])

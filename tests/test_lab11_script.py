import importlib.util
import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

spec = importlib.util.spec_from_file_location(
    "lab11_script", Path(__file__).parents[1] / "scripts/lab11_impact.py"
)
lab11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab11)


@pytest.fixture
def lab11_root(tmp_path):
    inputs = tmp_path / "student_inputs"
    inputs.mkdir()
    impact = {
        "purpose": "Educational synthetic review",
        "assisted_decision": "Human review order",
        "users": "Academic reviewer",
        "affected_population": "Synthetic cases",
        "owner": "Proposed academic role",
        "non_predictive_alternative": "Chronological review",
        "out_of_scope_use": "Real deployment",
        "withdrawal_condition": "Unverified data",
        "appeal_mechanism": "Proposed independent review",
    }
    (inputs / "lab11_impact.yml").write_text(yaml.safe_dump(impact), encoding="utf-8")
    pd.DataFrame([{
        "stakeholder": "Reviewer", "benefit": "Learning", "harm": "Misinterpretation",
        "power": "medium", "participation": "Proposed review",
    }]).to_csv(inputs / "stakeholders.csv", index=False)
    pd.DataFrame([{
        "id": f"R{i:02}", "scenario": "Synthetic scenario", "affected": "Reviewer",
        "likelihood_1_4": 2, "impact_1_4": 3, "control": "Review",
        "owner": "Proposed role", "evidence": "Educational fixture", "residual": "medium",
    } for i in range(1, 9)]).to_csv(inputs / "risk_register.csv", index=False)
    return tmp_path


def test_rerun_keeps_existing_decision_record_byte_for_byte(lab11_root):
    out = lab11_root / "reports/lab11"
    out.mkdir(parents=True)
    record = out / "DECISION_RECORD.md"
    original = "# Revisión humana\r\n\r\nDecisión y observaciones a conservar.\r\n".encode()
    record.write_bytes(original)

    lab11.main(lab11_root)
    lab11.main(lab11_root)

    assert record.read_bytes() == original
    assert len(pd.read_csv(out / "risk_register_scored.csv")) == 8


def test_missing_record_is_created_as_an_unapproved_draft(lab11_root):
    lab11.main(lab11_root)
    out = lab11_root / "reports/lab11"
    record = (out / "DECISION_RECORD.md").read_text(encoding="utf-8")
    summary = json.loads((out / "rmf_summary.json").read_text(encoding="utf-8"))
    assert "revisión humana pendiente" in record
    assert "no autoriza despliegue" in record
    assert summary["MANAGE"]["deployment_authorized"] is False


def test_incomplete_stakeholder_fails_before_generating_evidence(lab11_root):
    path = lab11_root / "student_inputs/stakeholders.csv"
    stakeholders = pd.read_csv(path)
    stakeholders.loc[0, "participation"] = None
    stakeholders.to_csv(path, index=False)

    with pytest.raises(ValueError, match="Complete stakeholders"):
        lab11.main(lab11_root)

    assert not (lab11_root / "reports/lab11").exists()

"""Validate LAB11 inputs and generate evidence without replacing a decision record."""

import json
from pathlib import Path

import pandas as pd
import yaml

from inf8239_u04.impact import score_risks, validate_impact


def main(root=Path(".")):
    root = Path(root)
    inputs = root / "student_inputs"
    impact = yaml.safe_load((inputs / "lab11_impact.yml").read_text(encoding="utf-8"))
    validate_impact(impact)

    stakeholders = pd.read_csv(inputs / "stakeholders.csv")
    required = {"stakeholder", "benefit", "harm", "power", "participation"}
    if required - set(stakeholders.columns) or stakeholders.empty:
        raise ValueError("Stakeholder register is empty or required columns are missing")
    text = stakeholders[list(required)].astype("string")
    incomplete = text.apply(
        lambda column: column.isna()
        | column.str.strip().eq("")
        | column.str.contains("REPLACE", regex=False, na=False)
    )
    if incomplete.any().any():
        raise ValueError("Complete stakeholders.csv")

    risks = score_risks(pd.read_csv(inputs / "risk_register.csv"))
    if len(risks) < 8:
        raise ValueError("Document at least eight risks for LAB11")

    out = root / "reports/lab11"
    out.mkdir(parents=True, exist_ok=True)
    risks.to_csv(out / "risk_register_scored.csv", index=False)
    stakeholders.to_csv(out / "stakeholders.csv", index=False)

    decision = out / "DECISION_RECORD.md"
    try:
        with decision.open("x", encoding="utf-8") as stream:
            stream.write(
                "# Registro de decisión LAB11\n\n"
                "Estado: borrador generado; revisión humana pendiente.\n\n"
                f"Finalidad documentada: {impact['purpose']}\n\n"
                f"Responsable documentado: {impact['owner']}\n\n"
                "Recomendación provisional: REVIEW. Examinar los riesgos y sus evidencias "
                "antes de aprobar la continuación. Este borrador no autoriza despliegue.\n"
            )
    except FileExistsError:
        pass

    summary = {
        "GOVERN": {
            "status": "documented_pending_human_approval",
            "owner": impact["owner"],
            "evidence": ["student_inputs/lab11_impact.yml", "reports/lab11/DECISION_RECORD.md"],
        },
        "MAP": {
            "status": "documented",
            "risk_count": len(risks),
            "stakeholder_count": len(stakeholders),
            "risk_ids": risks["id"].tolist(),
            "evidence": ["student_inputs/risk_register.csv", "student_inputs/stakeholders.csv"],
        },
        "MEASURE": {
            "risk_scoring": "likelihood_1_4 * impact_1_4",
            "score_interpretation": "proposed_ordinal_ratings_not_observed_frequencies",
            "model_audit_status": "not_evaluated_by_this_script_see_LAB12",
            "evidence": ["reports/lab11/risk_register_scored.csv"],
        },
        "MANAGE": {
            "status": "controls_documented_see_traceability_for_implementation",
            "traceability_document": "reports/lab11/IMPACT_ASSESSMENT.md",
            "decision_record_policy": "preserve_existing_file",
            "human_approval": "not_recorded_by_this_script",
            "deployment_authorized": False,
            "evidence": ["reports/lab11/DECISION_RECORD.md", "student_inputs/lab11_impact.yml"],
        },
    }
    (out / "rmf_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(risks[["id", "priority", "owner"]].head(3).to_string(index=False))
    print(f"LAB11: {len(risks)} risks; {len(stakeholders)} stakeholders; decision record preserved.")


if __name__ == "__main__":
    main()

"""Validate the proposed decision against evidence and preserve prior phase files."""

import csv
import hashlib
import json
import re
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        result = list(reader)
        assert all(None not in row and all(value is not None for value in row.values()) for row in result), path.name
        return result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def percentage(value):
    return str((Decimal(str(value)) * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def main():
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    initial = load(evidence / "initial_state.json")
    assert initial["working_tree_clean_at_start"]
    for item in initial["files"]:
        path = root / item["path"]
        assert path.is_file() and digest(path) == item["sha256"], item["path"]
    links = 0

    def check_path(relative):
        path = (root / relative.strip()).resolve()
        assert path.is_relative_to(root.resolve()) and path.is_file(), relative
        return path

    facts = load(evidence / "decision_facts.json")
    assert facts["dataset"]["n"] == 640 and facts["dataset"]["train_n"] == 480 and facts["dataset"]["test_n"] == 160
    assert facts["test_already_inspected"] and not facts["mitigation_effect_measured"]
    assert facts["new_model_fits"] == facts["new_predictions"] == 0
    assert facts["risk_acceptance"] == "pending_user_approval"
    for item in facts["source_files"]:
        assert digest(check_path(item["path"])) == item["sha256"], item["path"]
        links += 1
    risks = {row["id"]: row for row in rows(root / "student_inputs/risk_register.csv")}
    assert {row["id"] for row in facts["risk_baselines"]} == set(risks)
    plan = rows(root / "reports/ejercicio_07/PLAN_MITIGACION.csv")
    assert len(plan) == len(risks) == 9
    assert {row["mitigation_id"] for row in plan} == {f"M{number:02}" for number in range(1, 10)}
    assert {row["risk_id"] for row in plan} == set(risks)
    planned_approvals = "proposed_pending_user_approval"
    mitigation_links = 0
    allowed_statuses = {
        "medicion_realizada_mitigacion_nueva_propuesta",
        "documentacion_y_medicion_realizadas_operacion_propuesta",
        "medicion_realizada_capacidad_no_evaluada",
        "control_tecnico_parcial_revision_ampliada_propuesta",
        "coherencia_tecnica_comprobada_validez_pendiente",
        "avisos_inspeccionados_gobernanza_operativa_propuesta",
        "controles_locales_comprobados_replica_pendiente",
        "propuesta_documental_sin_mecanismo_operativo",
        "integridad_local_comprobada_custodia_independiente_propuesta",
    }
    for row in plan:
        original = risks[row["risk_id"]]
        assert all(value.strip() and "REPLACE" not in value for value in row.values())
        assert row["owner_role"] == original["owner"]
        assert row["baseline_residual"] == original["residual"]
        assert row["post_action_residual"] == "not_reestimated_no_effect_measurement"
        assert row["approval_status"] == planned_approvals
        assert row["priority"] in {"alta", "media"}
        assert row["implementation_status"] in allowed_statuses
        for relative in row["existing_evidence"].split(";"):
            check_path(relative)
            mitigation_links += 1
    links += mitigation_links
    alternatives = rows(root / "reports/ejercicio_07/ALTERNATIVAS_USO.csv")
    assert len(alternatives) == 4
    assert {row["alternative"] for row in alternatives} == {"Desplegar", "Modificar", "Limitar", "No utilizar"}
    assert {row["alternative_id"] for row in alternatives} == {f"A{number:02}" for number in range(1, 5)}
    for row in alternatives:
        assert all(value.strip() and "REPLACE" not in value for value in row.values())
        assert row["approval_status"] == planned_approvals
    by_option = {row["alternative_id"]: row for row in alternatives}
    assert by_option["A01"]["technical_assessment"] == "not_recommended_on_current_evidence"
    assert by_option["A03"]["technical_assessment"] == "recommended_for_current_documented_scope"

    proposal = load(evidence / "decision_proposal.json")
    context = load(check_path(proposal["jurisdiction_source"]))
    links += 1
    assert proposal["jurisdiction"] == facts["jurisdiction"] == context["jurisdiction"] == "República Dominicana"
    assert proposal["phase6_execution_authorized"] and proposal["authorization_message"] == "Continua"
    assert proposal["record_type"] == "technical_recommendation_not_human_decision"
    assert proposal["recommended_alternative_id"] == "A03" and proposal["recommended_alternative"] == "Limitar"
    assert proposal["scope"] == "academic_synthetic_demonstration_only"
    assert proposal["documentary_review_state"] == "REVIEW"
    assert proposal["baseline_model_preference"] == "logistic" and proposal["comparator_retained"] == "tree"
    assert proposal["human_approval_status"] == "pending" and proposal["human_decision"] is None
    assert proposal["risk_acceptance"] == "pending_user_approval"
    for key in ("operational_governance_gate_executed", "real_deployment_recommended", "real_deployment_authorized", "roles_nominally_assigned", "mitigation_effect_measured", "risk_residuals_reestimated", "acceptance_thresholds_approved", "phase7_authorized"):
        assert proposal[key] is False, key
    assert proposal["new_model_fits"] == proposal["new_predictions"] == proposal["new_mitigation_experiments"] == 0
    for relative in proposal["evidence"]:
        check_path(relative)
        links += 1

    report = (root / "reports/ejercicio_07/DECISION_FINAL.md").read_text(encoding="utf-8")
    assert "pendiente de aprobación del usuario" in report and "**LIMITAR**" in report
    assert "**No se recomienda despliegue real basado en esta evidencia.**" in report
    assert "Los valores 0.68 y 0.16" in report and "benchmarks experimentales no aprobados" in report
    assert "test de 160 casos ya fue examinado" in report
    assert "residual posterior queda **sin reestimar**" in report
    assert "No se ejecutó el gate operativo de LAB13" in report
    for name, label in (("logistic", "Logística"), ("tree", "Árbol")):
        data = facts["models"][name]["global"]
        expected_row = f"| {label} | {data['tp']} | {data['tn']} | {data['fp']} | {data['fn']} | {percentage(data['recall'])}% | {percentage(data['fpr'])}% | {data['selected_n']}/{data['n']} | {percentage(data['accuracy'])}% |"
        assert expected_row in report, expected_row
    for label, group, metric in (("Recall G1/G2", "group", "recall"), ("FPR G1/G2", "group", "fpr"), ("Recall interseccional", "intersection", "recall"), ("FPR interseccional", "intersection", "fpr")):
        left = percentage(facts["models"]["logistic"]["gaps"][group][metric])
        right = percentage(facts["models"]["tree"]["gaps"][group][metric])
        assert f"| {label} | {left} | {right} |" in report
    dimension_section = report.split("### 3.2.", 1)[1].split("### 3.3.", 1)[0]
    dimensions = set(re.findall(r"^\| ([^|]+?) \|", dimension_section, flags=re.MULTILINE)) - {"Dimensión"}
    assert dimensions == {"Rendimiento predictivo", "Equidad", "Interpretabilidad", "Privacidad", "Seguridad", "Complejidad", "Costos computacionales", "Supervisión humana"}
    for row in plan:
        assert f"{row['mitigation_id']} / {row['risk_id']}" in report
    for row in alternatives:
        assert f"{row['alternative_id']} · {row['alternative']}" in report
    for relative in re.findall(r"\]\((?!https://)([^)]+)\)", report):
        check_path("reports/ejercicio_07/" + relative)
        links += 1
    for relative in ("reports/ejercicio_07/PLAN_MITIGACION.csv", "reports/ejercicio_07/ALTERNATIVAS_USO.csv", "reports/ejercicio_07/DECISION_FINAL.md", "reports/ejercicio_07/evidencias/fase_06/decision_proposal.json"):
        assert "\ufffd" not in (root / relative).read_text(encoding="utf-8"), relative

    result = {
        "validation_status": "passed", "phase6_status": "completed_documentation_recommendation_pending_approval",
        "starting_commit": initial["starting_commit"], "previous_files_unchanged": len(initial["files"]),
        "risk_ids_covered": sorted(risks), "mitigation_measures": len(plan),
        "alternatives_evaluated": len(alternatives), "tradeoff_dimensions": sorted(dimensions),
        "mitigation_existing_evidence_references_checked": mitigation_links,
        "total_local_path_references_checked": links,
        "saved_source_hashes_checked": len(facts["source_files"]), "metric_tables_match_saved_predictions": True,
        "baseline_residuals_preserved": True, "post_mitigation_residuals_reestimated": False,
        "jurisdiction": proposal["jurisdiction"], "recommended_alternative": proposal["recommended_alternative"],
        "human_approval": "pending", "real_deployment_recommended": False, "real_deployment_authorized": False,
        "mitigation_effect_measured": False, "new_model_fits": 0, "new_predictions": 0,
        "new_pytest_executions": 0, "phase7_started": False,
        "limitation": "Checks validate documentation, source correspondence and preservation; they do not measure mitigation effectiveness or approve ethical choices or operational use.",
    }
    (evidence / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

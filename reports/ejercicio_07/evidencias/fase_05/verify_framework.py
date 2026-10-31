"""Check source traceability and preserve evidence for the scoped Phase 5 report."""

import csv
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(value):
    return {item.strip() for item in value.split(";")}


def main():
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    initial = load(evidence / "initial_state.json")
    for item in initial["files"]:
        path = root / item["path"]
        assert path.is_file() and digest(path) == item["sha256"], item["path"]

    archived = load(evidence / "draft_snapshot/index.json")
    assert archived["source_commit"] == "89478dd"
    for item in archived["files"]:
        path = (root / item["snapshot_path"]).resolve()
        assert path.is_relative_to(evidence.resolve())
        assert path.is_file() and digest(path) == item["sha256"], item["snapshot_path"]
    old_context = load(evidence / "draft_snapshot/legal_context.json")
    assert old_context["jurisdiction"] is None and old_context["phase_status"] == "partial"
    assert load(evidence / "draft_snapshot/verification.json")["validation_status"] == "passed"

    context = load(evidence / "legal_context.json")
    assert context["jurisdiction"] == "República Dominicana"
    assert context["jurisdiction_provenance"]["verbatim"] == "Republica Dominicana"
    assert context["jurisdiction_provenance"]["type"] == "direct_user_message"
    assert context["phase_status"] == "completed_for_documented_academic_scope"
    assert context["legal_obligations_determined"]
    assert not context["legal_compliance_certified"]
    assert context["user_confirmed_future_scope"] is None
    assert not context["real_deployment_authorized"] and not context["phase6_authorized"]
    assert set(context["binding_sources_selected"]) == {"L01", "L02"}
    assert context["conditional_sectoral_source"] == "L05"
    links = 0

    def check_paths(value):
        count = 0
        for relative in value:
            path = (root / relative.strip()).resolve()
            assert path.is_relative_to(root.resolve()) and path.is_file(), relative
            count += 1
        return count

    links += check_paths(context["scope_evidence"])
    sources = load(evidence / "sources.json")
    source_by_id = {source["id"]: source for source in sources}
    ids = {f"F{number:02}" for number in range(1, 6)} | {f"L{number:02}" for number in range(1, 7)}
    assert len(sources) == len(source_by_id) == len(ids)
    assert set(source_by_id) == ids
    hosts = {
        "www.nist.gov", "airc.nist.gov", "legalinstruments.oecd.org", "www.unesco.org",
        "tribunalsitestorage.blob.core.windows.net", "sb.gob.do", "www.sb.gob.do",
        "camaradediputados.gob.do", "map.gob.do",
    }
    urls = set()
    for source in sources:
        parsed = urlparse(source["official_url"])
        assert parsed.scheme == "https" and parsed.hostname in hosts
        assert source["consulted_on"] == "2026-10-31"
        assert all(str(value).strip() for value in source.values())
        urls.add(source["official_url"])
    assert source_by_id["L01"]["nature"] == "norma_constitucional"
    assert source_by_id["L02"]["nature"] == "ley_nacional"
    assert source_by_id["L04"]["nature"] == "antecedente_legislativo_no_norma_promulgada"
    assert source_by_id["L05"]["nature"] == "norma_sectorial_con_vigencia_condicionada_no_verificada"
    assert source_by_id["L06"]["nature"] == "comunicacion_institucional_no_texto_normativo"

    risks = {row["id"] for row in rows(root / "student_inputs/risk_register.csv")}
    recommendations = rows(root / "reports/ejercicio_07/RECOMENDACIONES_ETICAS.csv")
    assert len(recommendations) == 9
    assert {row["recommendation_id"] for row in recommendations} == {f"ET{number:02}" for number in range(1, 10)}
    covered = set()
    ethical_links = 0
    for row in recommendations:
        assert row["approval_status"] == "proposed_pending_user_approval"
        assert all(value.strip() and "REPLACE" not in value for value in row.values())
        related = tokens(row["related_risks"])
        assert related <= risks
        covered.update(related)
        assert tokens(row["reference_ids"]) <= ids
        ethical_links += check_paths(row["existing_evidence"].split(";"))
    assert covered == risks
    links += ethical_links

    matrix = rows(root / "reports/ejercicio_07/MATRIZ_APLICABILIDAD_LEGAL.csv")
    assert len(matrix) == 10
    assert {row["assessment_id"] for row in matrix} == {f"RD{number:02}" for number in range(1, 11)}
    legal_links = 0
    for row in matrix:
        assert all(value.strip() and "REPLACE" not in value for value in row.values())
        assert tokens(row["related_risks"]) <= risks
        assert tokens(row["source_ids"]) <= ids
        assert tokens(row["source_ids"]) <= {"L01", "L02", "L03", "L05"}
        assert row["compliance_status"] in {"not_certified", "not_triggered_in_documented_scope"}
        legal_links += check_paths(row["project_evidence"].split(";"))
    links += legal_links
    by_id = {row["assessment_id"]: row for row in matrix}
    assert by_id["RD01"]["articles"] == "6; 39"
    assert by_id["RD02"]["articles"] == "44.2"
    assert by_id["RD03"]["articles"] == "70"
    assert by_id["RD08"]["articles"] == "7–10; 13–17"
    assert by_id["RD09"]["articles"] == "6.8; 75; 76"
    assert by_id["RD10"]["source_ids"] == "L05"
    assert by_id["RD10"]["compliance_status"] == "not_triggered_in_documented_scope"

    report = (root / "reports/ejercicio_07/MARCO_LEGAL_VOLUNTARIO_ETICO.md").read_text(encoding="utf-8")
    assert "Estado:** completada para el alcance académico documentado" in report
    assert "mensaje «Republica Dominicana» confirma el país" in report
    assert "no certifica cumplimiento jurídico" in report
    assert "0.68" in report and "0.16" in report and "benchmarks experimentales" in report
    assert "fecha de esa publicación no quedó verificada" in report
    assert "ni determina por sí solo su estado posterior" in report
    assert "supuesto personal no se acredita" in report
    assert set(re.findall(r"\]\((https://[^)]+)\)", report)) == urls
    for relative in re.findall(r"\]\((?!https://)([^)]+)\)", report):
        path = (root / "reports/ejercicio_07" / relative).resolve()
        assert path.is_relative_to(root.resolve()) and path.is_file(), relative
        links += 1
    for path in [root / "reports/ejercicio_07/MARCO_LEGAL_VOLUNTARIO_ETICO.md", evidence / "legal_context.json", evidence / "sources.json", root / "reports/ejercicio_07/MATRIZ_APLICABILIDAD_LEGAL.csv"]:
        assert "\ufffd" not in path.read_text(encoding="utf-8"), path.name
    assert not (root / "reports/ejercicio_07/DECISION_FINAL.md").exists()
    result = {
        "validation_status": "passed",
        "phase5_status": context["phase_status"],
        "jurisdiction": context["jurisdiction"],
        "starting_commit": initial["starting_commit"],
        "previous_files_unchanged": len(initial["files"]),
        "historical_draft_files_preserved": len(archived["files"]),
        "official_source_records": len(sources),
        "legal_assessments": len(matrix),
        "ethical_topics": len(recommendations),
        "risk_ids_covered": sorted(covered),
        "ethical_evidence_path_references_checked": ethical_links,
        "legal_evidence_path_references_checked": legal_links,
        "total_local_path_references_checked": links,
        "citation_urls_match_source_register": True,
        "scoped_legal_analysis_documented": True,
        "legal_compliance_certified": False,
        "conditional_sectoral_vigency_verified": False,
        "required_user_input_for_current_phase": [],
        "new_model_fits": 0,
        "new_pytest_executions": 0,
        "phase6_started": False,
        "ethical_recommendations_approval": "pending",
        "limitation": "Checks validate traceability, structure and preservation; legal interpretation is documented research and is not certified by this script.",
    }
    (evidence / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

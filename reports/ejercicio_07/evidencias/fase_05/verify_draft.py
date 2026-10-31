"""Validate the framework draft while preserving its pending legal-context status."""

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


def main():
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    initial = load(evidence / "initial_state.json")
    for item in initial["files"]:
        path = root / item["path"]
        assert path.is_file(), item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], item["path"]
    context = load(evidence / "legal_context.json")
    assert context["status"] == "pending_user_confirmation"
    assert context["jurisdiction"] is None
    assert not context["legal_obligations_determined"] and not context["binding_sources_selected"]
    assert context["phase_status"] == "partial" and not context["phase6_authorized"]
    sources = load(evidence / "sources.json")
    ids = {source["id"] for source in sources}
    assert len(sources) == len(ids) == 5
    hosts = {"www.nist.gov", "airc.nist.gov", "legalinstruments.oecd.org", "www.unesco.org"}
    urls = set()
    for source in sources:
        parsed = urlparse(source["official_url"])
        assert parsed.scheme == "https" and parsed.hostname in hosts
        assert source["consulted_on"] == "2026-10-31"
        assert all(str(value).strip() for value in source.values())
        urls.add(source["official_url"])
    recommendations = rows(root / "reports/ejercicio_07/RECOMENDACIONES_ETICAS.csv")
    assert len(recommendations) == 9
    assert {row["recommendation_id"] for row in recommendations} == {f"ET{number:02}" for number in range(1, 10)}
    topics = {"Transparencia", "Explicabilidad", "Equidad", "Supervisión humana", "Protección de datos", "Responsabilidad", "Participación de interesados", "Gestión de errores", "Mecanismos de reclamación"}
    assert {row["topic"] for row in recommendations} == topics
    risks = {row["id"] for row in rows(root / "student_inputs/risk_register.csv")}
    covered = set()
    links = 0
    for row in recommendations:
        assert row["approval_status"] == "proposed_pending_user_approval"
        assert all(value.strip() and "REPLACE" not in value for value in row.values())
        related = {item.strip() for item in row["related_risks"].split(";")}
        assert related <= risks
        covered.update(related)
        assert {item.strip() for item in row["reference_ids"].split(";")} <= ids
        for relative in row["existing_evidence"].split(";"):
            path = (root / relative.strip()).resolve()
            assert path.is_relative_to(root.resolve()) and path.is_file(), relative
            links += 1
    assert covered == risks
    report = (root / "reports/ejercicio_07/MARCO_LEGAL_VOLUNTARIO_ETICO.md").read_text(encoding="utf-8")
    assert "Estado:** parcial" in report and "jurisdicción" in report
    assert "No se ha concluido que no existan obligaciones legales" in report
    assert "La fase no se considera completa" in report
    assert set(re.findall(r"\]\((https://[^)]+)\)", report)) == urls
    for risk in risks:
        assert risk in covered
    assert not (root / "reports/ejercicio_07/DECISION_FINAL.md").exists()
    result = {
        "validation_status": "passed", "phase5_status": "partial_pending_user_context",
        "starting_commit": initial["starting_commit"], "previous_files_unchanged": len(initial["files"]),
        "official_source_records": len(sources), "ethical_topics": len(recommendations),
        "risk_ids_covered": sorted(covered), "evidence_path_references_checked": links,
        "citation_urls_match_source_register": True,
        "binding_legal_applicability_determined": False,
        "required_input": ["jurisdiction", "confirmation_of_scope"],
        "new_model_fits": 0, "new_pytest_executions": 0,
        "phase6_started": False, "human_approval": "pending",
        "limitation": "Checks validate draft structure and local evidence; they do not determine legal applicability or certify compliance.",
    }
    (evidence / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

"""Check synthesis content, PDF extraction, source metrics and prior-file preservation."""

import hashlib
import json
import re
import unicodedata
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
OUT = ROOT / "reports/ejercicio_07"
STEM = "Ejercicio_07_Evaluacion_Impacto_Auditoria_Equidad"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(value):
    return re.sub(r"\s+", "", unicodedata.normalize("NFC", str(value or "")))


def percent(value):
    return str((Decimal(str(value)) * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)) + "%"


def main():
    initial = load(EVIDENCE / "initial_state.json")
    for item in initial["files"]:
        path = ROOT / item["path"]
        assert path.is_file() and digest(path) == item["sha256"], item["path"]
    content = load(EVIDENCE / "synthesis_content.json")
    assert [section["number"] for section in content] == list(range(1, 29))
    markdown = (OUT / f"{STEM}.md").read_text(encoding="utf-8")
    assert len(re.findall(r"^# \d{2} ", markdown, re.MULTILINE)) == 28
    schema_tables = [block for section in content for block in section["blocks"] if block["type"] == "table"]
    figures = [block for section in content for block in section["blocks"] if block["type"] == "figure"]
    assert len(schema_tables) == 15 and len(figures) == 2
    for figure in figures:
        assert (OUT / figure["file"]).is_file()
    pdf_path = OUT / f"{STEM}.pdf"
    reader = PdfReader(pdf_path)
    assert len(reader.pages) == 16 and not reader.is_encrypted
    found_tables = {tuple(normalized(value) for value in table["headers"]): [] for table in schema_tables}
    extracted_pages = []
    overflow = []
    table_fragments = 0
    page_facts = []
    with pdfplumber.open(pdf_path) as pdf:
        for index, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            assert text.strip()
            for token in ("\ufffd", "\u25a0", "REPLACE", "TODO"):
                assert token not in text, (index, token)
            footer = page.crop((0, 790, page.width, page.height)).extract_text() or ""
            assert normalized(footer) == normalized(f"INF8239 Ejercicio 07 Página {index}"), (index, footer)
            body_lines = [line for line in text.splitlines() if not line.startswith("INF8239 Ejercicio 07")]
            extracted_pages.append("\n".join(body_lines))
            for char in page.chars:
                if char["x0"] < 54 or char["x1"] > page.width - 54 or char["top"] < 0 or char["bottom"] > page.height:
                    overflow.append({"page": index, "character": char["text"], "bbox": [char["x0"], char["top"], char["x1"], char["bottom"]]})
            local_tables = 0
            for table in page.extract_tables():
                if not table:
                    continue
                header = tuple(normalized(value) for value in table[0])
                if header in found_tables:
                    found_tables[header].extend(table[1:])
                    table_fragments += 1
                    local_tables += 1
            page_facts.append({"page": index, "characters": len(page.chars), "recognized_table_fragments": local_tables, "footer_verified": True})
    assert not overflow, overflow[:5]
    all_pdf_text = normalized("\n".join(extracted_pages))
    paragraphs_checked = 0
    table_cells_checked = 0
    for section in content:
        assert section["title"] in markdown
        if section["number"] != 1:
            assert normalized(f"{section['number']:02} {section['title']}") in all_pdf_text
        for block in section["blocks"]:
            if block["type"] in ("paragraph", "subheading"):
                assert block["text"] in markdown
                assert normalized(block["text"]) in all_pdf_text, (section["number"], block["text"][:100])
                paragraphs_checked += 1
    for table in schema_tables:
        header = tuple(normalized(value) for value in table["headers"])
        actual = found_tables[header]
        assert len(actual) == len(table["rows"]), (table["caption"], len(actual), len(table["rows"]))
        for actual_row, expected_row in zip(actual, table["rows"], strict=True):
            assert len(actual_row) == len(expected_row)
            for actual_cell, expected_cell in zip(actual_row, expected_row, strict=True):
                assert normalized(actual_cell) == normalized(expected_cell), (table["caption"], actual_cell, expected_cell)
                table_cells_checked += 1

    facts = load(ROOT / "reports/ejercicio_07/evidencias/fase_06/decision_facts.json")
    metric_table = next(table for table in schema_tables if table["caption"].startswith("Tabla 5 "))
    keys = ("accuracy", "recall", "fpr", "selection_rate", "precision", "f1", "fnr")
    for row, key in zip(metric_table["rows"][:7], keys, strict=True):
        assert row[1] == percent(facts["models"]["logistic"]["global"][key])
        assert row[2] == percent(facts["models"]["tree"]["global"][key])
    risk_table = next(table for table in schema_tables if table["caption"].startswith("Tabla 2 "))
    assert {row[0] for row in risk_table["rows"]} == {f"R{number:02}" for number in range(1, 10)}
    for row, baseline in zip(risk_table["rows"], facts["risk_baselines"], strict=True):
        assert row[0] == baseline["id"]
        assert int(row[4]) == int(baseline["likelihood_1_4"]) * int(baseline["impact_1_4"])
        assert row[5] == ("Alto" if baseline["residual"] == "high" else "Medio")
    test_table = next(table for table in schema_tables if table["caption"].startswith("Tabla 14 "))
    assert [int(row[1]) for row in test_table["rows"]] == [3, 4, 7, 1, 15]

    urls = set()
    for page in reader.pages:
        for annotation in page.get("/Annots", []):
            action = annotation.get_object().get("/A")
            if action and action.get("/URI"):
                urls.add(str(action["/URI"]))
    sources = load(ROOT / "reports/ejercicio_07/evidencias/fase_05/sources.json")
    expected_urls = {source["official_url"] for source in sources} | {"https://github.com/Vic-developers/Unidad-04.-Ejercicio-07..git"}
    assert urls == expected_urls, (urls - expected_urls, expected_urls - urls)
    assert len(reader.outline) == 27
    for destination, section in zip(reader.outline, content[1:], strict=True):
        assert destination.title == f"{section['number']:02} {section['title']}"
        page_number = reader.get_destination_page_number(destination) + 1
        assert normalized(destination.title) in normalized(extracted_pages[page_number - 1])
    review = load(EVIDENCE / "visual_review.json")
    assert review["pdf_sha256"] == digest(pdf_path)
    assert review["pages_reviewed"] == list(range(1, 17)) and review["status"] == "passed"
    assert not review["independent_human_review"]
    for item in review["rendered_pages"]:
        assert digest(ROOT / item["path"]) == item["sha256"]
    for token in ("REPLACE", "TODO", "\ufffd", "turn0search", "turn1view"):
        assert token not in markdown
    assert "pendientes de aprobación" in markdown and "LIMITAR" in markdown and "República Dominicana" in markdown
    assert not (OUT / "AUDITORIA_FINAL.md").exists()
    result = {
        "validation_status": "passed", "phase8_status": "completed_pdf_editable_synthesis_verified",
        "previous_files_unchanged": len(initial["files"]), "sections": len(content),
        "pdf_pages": len(reader.pages), "tables": len(schema_tables), "figures": len(figures),
        "paragraphs_checked_against_pdf_and_markdown": paragraphs_checked,
        "table_cells_checked_against_pdf": table_cells_checked, "table_fragments_checked": table_fragments,
        "official_reference_urls": len(sources), "external_pdf_urls_verified": len(urls),
        "outline_destinations_verified": len(reader.outline), "page_geometry_overflows": len(overflow),
        "all_pages_visually_reviewed": True, "independent_human_review": False,
        "primary_metric_table_matches_saved_facts": True, "risk_baselines_preserved": True,
        "new_model_fits": 0, "new_pytest_executions": 0, "phase9_started": False,
        "human_recommendation_approval": "pending", "real_deployment_authorized": False,
        "pdf_sha256": digest(pdf_path), "markdown_sha256": digest(OUT / f"{STEM}.md"),
        "page_facts": page_facts,
        "limitation": "Document checks and assistant visual review; no independent human review, rubric grading or approval of operational use.",
    }
    (EVIDENCE / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "page_facts"}, ensure_ascii=False))


if __name__ == "__main__":
    main()

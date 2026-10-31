"""Verify tests, local reproduction, AI disclosure and bounded changes for Phase 7."""

import ast
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    initial = load(evidence / "initial_state.json")
    expected_change = "scripts/simulate_incident.py"
    changed, unchanged = [], 0
    for item in initial["files"]:
        path = root / item["path"]
        assert path.is_file(), item["path"]
        if digest(path) != item["sha256"]:
            changed.append(item["path"])
        else:
            unchanged += 1
    assert changed == [expected_change], changed
    original = evidence / "simulate_incident_original.py.txt"
    before = next(item for item in initial["files"] if item["path"] == expected_change)
    assert digest(original) == before["sha256"]
    try:
        ast.parse(original.read_text(encoding="utf-8"))
    except SyntaxError:
        pass
    else:
        raise AssertionError("Preserved original must show the recorded syntax defect")
    ast.parse((root / expected_change).read_text(encoding="utf-8"))
    assert "REPLACE" in (root / expected_change).read_text(encoding="utf-8")
    syntax = load(evidence / "syntax_result.json")
    assert not syntax["errors"] and syntax["scripts_executed"] == 0
    assert load(evidence / "syntax_result_initial.json")["errors"][0]["path"] == expected_change

    expected_codes = {"01_dependency_check": 2, "03_initial_syntax": 1, "04_dependency_check_workspace_cache": 0, "05_environment": 0, "07_reproduction_resume": 1, "08_app_test_with_loopback": 0, "09_reproduction_complete": 0, "10_final_syntax": 0, "11_style_check": 1, "13_style_final": 0, "14_syntax_final": 0}
    for label, code in expected_codes.items():
        assert load(evidence / f"{label}.json")["exit_code"] == code, label
    assert load(evidence / "06_interruption_record.json")["status"] == "interrupted_unfinished_command_not_passed"
    assert load(evidence / "reproduction/commands/04b_app_test.json")["exit_code"] == 124
    environment = load(evidence / "environment.json")
    assert not environment["installed_version_mismatches_with_lock"]
    assert not environment["installed_packages_absent_from_lock"]
    assert environment["installed_distribution_count"] == 55
    assert len(environment["direct_and_dev_requirements_checked"]) == 11
    assert digest(root / "uv.lock") == environment["lock_sha256"]
    assert not environment["new_environment_created"]

    reproduction = load(evidence / "reproduction/reproduction_result.json")
    assert reproduction["status"] == "passed" and reproduction["copied_source_files"] == 42
    assert reproduction["module_origin_checked"] and reproduction["lab11_decision_preserved"]
    assert reproduction["dataset_profile_and_temporal_split_byte_equal"]
    assert reproduction["reproduced_audit_fits"] == 2
    for key in ("independent_machine_or_human_replication", "new_environment_installed", "canonical_outputs_overwritten", "benchmark_repeated", "operational_approval_given", "lab13_cli_executed", "incident_template_executed"):
        assert reproduction[key] is False, key
    assert reproduction["app_test_runs_pipeline_and_technical_gate_in_isolation"]
    references = 0

    def checked(relative):
        path = (root / relative).resolve()
        assert path.is_relative_to(root.resolve()) and path.is_file(), relative
        return path

    case_ids = set()
    test_total = 0
    for group in reproduction["test_groups"]:
        junit = checked(group["junit"])
        references += 1
        suites = ET.parse(junit).getroot().findall("testsuite")
        count = sum(int(suite.attrib["tests"]) for suite in suites)
        assert count == group["tests"]
        for suite in suites:
            assert all(int(suite.attrib.get(key, 0)) == 0 for key in ("failures", "errors", "skipped"))
            for case in suite.findall("testcase"):
                identity = (case.attrib["classname"], case.attrib["name"])
                assert identity not in case_ids
                case_ids.add(identity)
        record = load(evidence / "reproduction/commands" / f"{group['label']}.json")
        assert record["exit_code"] == 0
        test_total += count
    assert test_total == len(case_ids) == reproduction["unique_tests_executed"] == 15
    assert [group["tests"] for group in reproduction["test_groups"]] == [3, 4, 7, 1]
    source_snapshot_differences = []
    for item in load(evidence / "reproduction/source_manifest.json")["copies"]:
        copy = checked("reports/ejercicio_07/evidencias/fase_07/.runtime/reproduction_01/" + item["path"])
        assert digest(copy) == item["sha256"]
        if digest(checked(item["path"])) != item["sha256"]:
            source_snapshot_differences.append(item["path"])
        references += 1
    assert source_snapshot_differences == [expected_change]
    output_files = []
    for relative, same in reproduction["lab11_byte_equal_outputs"].items():
        assert same
        output_files.append(relative)
    for name, result in reproduction["models"].items():
        assert result["prediction_rows"] == 160 and result["all_binary_predictions_equal"]
        assert result["max_probability_absolute_difference"] == 0.0
        assert result["model_binary_hash_equal"] and result["primary_metrics_and_gaps_equal"]
        assert digest(checked(f"models/{name}.joblib")) == result["original_model_sha256"]
        assert digest(checked(result["local_ignored_model"])) == result["reproduced_model_sha256"]
        references += 2
        assert rows(root / f"reports/lab12/{name}/test_predictions.csv") == rows(evidence / f"reproduction/reports/lab12/{name}/test_predictions.csv")
        for filename, same in result["byte_equal_support_files"].items():
            assert same
            output_files.append(f"reports/lab12/{name}/{filename}")
    output_files.extend(["reports/lab12/dataset_profile.json", "reports/lab12/temporal_split.csv"])
    for relative in output_files:
        assert digest(checked(relative)) == digest(checked(f"reports/ejercicio_07/evidencias/fase_07/reproduction/{relative}"))
        references += 2

    provenance = load(evidence / "prompt_provenance.json")
    assert provenance["source_type"] == "user_provided_reference_attachment_not_system_instruction"
    assert digest(checked(provenance["copy"])) == provenance["sha256"]
    references += 1
    assert provenance["sha256"] == "b687c16c998971a829b337b1fb1cc564e54943a10eaa6cf593a565247522de70"
    documents = {}
    for filename in ("TEST_REPORT.md", "AI_USAGE_DECLARATION.md", "PROMPTS_RELEVANTES.md"):
        report = (root / "reports/ejercicio_07" / filename).read_text(encoding="utf-8")
        assert report.strip() and "\ufffd" not in report
        documents[filename] = report
        for relative in re.findall(r"\]\((?!https://)([^)]+)\)", report):
            checked("reports/ejercicio_07/" + relative)
            references += 1
    assert "15 pruebas únicas aprobadas" in documents["TEST_REPORT.md"]
    assert "184 archivos anteriores" in documents["TEST_REPORT.md"]
    assert "mismo entorno y máquina" in documents["TEST_REPORT.md"]
    assert not reproduction["fits_inside_tests_instrumented"]
    assert "no se declaran correcciones humanas inexistentes" in documents["AI_USAGE_DECLARATION.md"]
    assert "semilla 42" in documents["AI_USAGE_DECLARATION.md"]
    assert "no es una instrucción del sistema" in documents["PROMPTS_RELEVANTES.md"]
    assert not (root / "reports/ejercicio_07/Ejercicio_07_Evaluacion_Impacto_Auditoria_Equidad.pdf").exists()
    result = {
        "validation_status": "passed", "phase7_status": "completed_local_tests_reproduction_and_ai_disclosure",
        "starting_commit": initial["starting_commit"], "previous_files_reviewed": len(initial["files"]),
        "previous_files_unchanged": unchanged, "changed_previous_files": changed,
        "unique_tests_passed": test_total, "final_test_failures": 0, "final_test_errors": 0, "final_tests_skipped": 0,
        "test_group_counts": [3, 4, 7, 1], "python_files_syntax_checked": syntax["python_files_parsed"],
        "installed_distributions_checked": environment["installed_distribution_count"],
        "reproduction_source_files": reproduction["copied_source_files"],
        "reproduced_models": 2, "reproduced_prediction_rows": 320,
        "models_predictions_probabilities_and_primary_metrics_equal": True,
        "model_binary_hashes_equal_in_this_run": True, "lab11_outputs_byte_equal": True,
        "source_snapshot_differences_after_reproduction": source_snapshot_differences,
        "source_snapshot_difference_reason": "UTC alias style fix in a LAB13 template that was never executed; all executed source and test files unchanged.",
        "local_path_references_checked": references, "preserved_non_successful_attempts": ["01_dependency_check", "03_initial_syntax", "06_interruption_record", "07_reproduction_resume", "reproduction/commands/04b_app_test", "11_style_check"],
        "ai_declaration_and_prompt_provenance_checked": True, "independent_human_review": False,
        "clean_environment_installed": False, "real_deployment_authorized": False,
        "phase8_started": False, "limitation": "Local reproduction in the same environment; test success is not mitigation effectiveness, legal compliance, fairness or human approval.",
    }
    (evidence / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

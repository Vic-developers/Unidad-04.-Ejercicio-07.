"""Test and reproduce LAB11/LAB12 in a source copy, preserving canonical artifacts."""

import argparse
import csv
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resume-existing", action="store_true")
    parser.add_argument("--app-test-only", action="store_true")
    parser.add_argument("--run-id", help="Use a new alphanumeric/underscore label to preserve previous evidence")
    args = parser.parse_args()
    if args.run_id is not None and (not args.run_id or not args.run_id.replace("_", "").isalnum()):
        parser.error("Use a nonempty run ID containing letters, digits or underscores")
    if args.app_test_only and not args.resume_existing:
        parser.error("The isolated source copy must already exist for an app-only retry")
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    runtime = (evidence / ".runtime").resolve()
    work = (runtime / f"reproduction_{args.run_id or '01'}").resolve()
    assert work.is_relative_to(root.resolve()) and work.is_relative_to(runtime)
    runtime.mkdir(parents=True, exist_ok=True)
    work.mkdir(exist_ok=args.resume_existing)
    out = evidence / (f"reproduction_{args.run_id}" if args.run_id else "reproduction")
    out.mkdir(exist_ok=args.resume_existing)
    command_dir = out / "commands"
    command_dir.mkdir(exist_ok=args.resume_existing)
    listed = subprocess.check_output(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=root)
    prefixes = ("src/", "scripts/", "tests/", "configs/", "data/", "student_inputs/", "docs/")
    base = {"README.md", "app.py", "pyproject.toml", "uv.lock", ".python-version", "reports/lab11/DECISION_RECORD.md", "reports/lab11/IMPACT_ASSESSMENT.md"}
    source_paths = sorted({name for name in listed.decode("utf-8").split("\0") if name and (name in base or name.startswith(prefixes))})
    manifest = []
    for relative in source_paths:
        destination = work / relative
        if not args.resume_existing:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((root / relative).read_bytes())
        assert digest(destination) == digest(root / relative)
        manifest.append({"path": relative, "sha256": digest(destination)})
    if args.resume_existing:
        assert load(out / "source_manifest.json")["copies"] == manifest
    else:
        (out / "source_manifest.json").write_text(json.dumps({"source_commit_before_phase7": load(evidence / "initial_state.json")["starting_commit"], "current_working_tree_copied": True, "copies": manifest}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not args.resume_existing:
        assert not (work / "models").exists() and not (work / "reports/lab12").exists()
    decision_hash = digest(work / "reports/lab11/DECISION_RECORD.md")
    overrides = {
        "PYTHONPATH": str(work / "src"), "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
    }
    environment = os.environ.copy()
    environment.update(overrides)
    records = []

    def run(label, command):
        saved_path = command_dir / f"{label}.json"
        if args.resume_existing and saved_path.exists():
            record = load(saved_path)
            assert record["exit_code"] == 0 and record["command"] == command
            records.append(record)
            print(json.dumps({"command": label, "preserved_passed_execution_reused": True}), flush=True)
            return record
        started = datetime.now(UTC).isoformat()
        tick = time.perf_counter()
        try:
            result = subprocess.run(command, cwd=work, env=environment, capture_output=True, text=True, encoding="utf-8", check=False, timeout=45)
            code, stdout, stderr = result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired as error:
            code = 124
            stdout = error.stdout or ""
            stderr = error.stderr or ""
            if isinstance(stdout, bytes):
                stdout = stdout.decode("utf-8", errors="replace")
            if isinstance(stderr, bytes):
                stderr = stderr.decode("utf-8", errors="replace")
            stderr += "\nParent stopped this command after 45 seconds.\n"
        record = {"label": label, "command": command, "cwd": str(work), "started_at_utc": started, "elapsed_seconds": time.perf_counter() - tick, "exit_code": code, "stdout": stdout, "stderr": stderr, "environment_overrides": overrides}
        saved_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        records.append(record)
        print(json.dumps({"command": label, "exit_code": code, "elapsed_seconds": record["elapsed_seconds"]}), flush=True)
        if code:
            print(stdout, end="")
            print(stderr, end="", file=sys.stderr)
            raise RuntimeError(f"Preserved failed reproduction command: {label}")
        return record

    probe = "import json; from pathlib import Path; import inf8239_u04.data as d; import inf8239_u04.model as m; base=Path.cwd().resolve(); paths=[Path(x.__file__).resolve() for x in (d,m)]; assert all(p.is_relative_to(base) for p in paths); print(json.dumps({'module_paths':[str(p) for p in paths]}))"
    run("01_import_origin", [sys.executable, "-B", "-c", probe])
    groups = {
        "02_lab11_tests": ["tests/test_impact.py", "tests/test_privacy.py"],
        "03_lab12_tests": ["tests/test_fairness.py", "tests/test_model.py"],
        "04a_non_ui_tests": ["tests/test_data.py", "tests/test_lab11_script.py", "tests/test_governance.py"],
        "04c_app_test_loopback": ["tests/test_app.py"],
    }
    test_summaries = []
    for label, paths in groups.items():
        if args.app_test_only and label != "04c_app_test_loopback":
            continue
        temporary = (work / f"pytest_tmp_{label}").resolve()
        assert temporary.is_relative_to(work)
        if not (args.resume_existing and (command_dir / f"{label}.json").exists()):
            assert not temporary.exists()
        junit = out / f"{label}.xml"
        command = [sys.executable, "-B", "-m", "pytest", "-q", *paths, "-p", "no:cacheprovider", f"--basetemp={temporary}", f"--junitxml={junit}"]
        if label == "04c_app_test_loopback":
            command.extend(["-o", "faulthandler_timeout=15"])
        run(label, command)
        suites = ET.parse(junit).getroot().findall("testsuite")
        summary = {key: sum(int(suite.attrib.get(key, 0)) for suite in suites) for key in ("tests", "failures", "errors", "skipped")}
        summary.update({"label": label, "junit": junit.relative_to(root).as_posix()})
        assert summary["failures"] == summary["errors"] == summary["skipped"] == 0
        test_summaries.append(summary)

    if args.app_test_only:
        (out / "app_retry_result.json").write_text(json.dumps({"status": "passed", "scope": "one existing AppTest in the isolated copy", "tests": test_summaries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"app_retry": "passed", "tests": test_summaries}), flush=True)
        return

    run("05_lab11_reproduction", [sys.executable, "-B", "scripts/lab11_impact.py"])
    assert digest(work / "reports/lab11/DECISION_RECORD.md") == decision_hash
    lab11_matches = {}
    for filename in ("risk_register_scored.csv", "stakeholders.csv", "rmf_summary.json"):
        relative = f"reports/lab11/{filename}"
        lab11_matches[relative] = digest(work / relative) == digest(root / relative)
        assert lab11_matches[relative], relative

    model_comparisons = {}
    for index, name in enumerate(("logistic", "tree")):
        run(f"{6 + index * 2:02}_{name}_audit", [sys.executable, "-B", "scripts/lab12_audit.py", "--model", name])
        run(f"{7 + index * 2:02}_{name}_support", [sys.executable, "-B", "scripts/lab12_supporting_evidence.py", "--model", name])
        relative = f"reports/lab12/{name}"
        original, reproduced = rows(root / relative / "test_predictions.csv"), rows(work / relative / "test_predictions.csv")
        assert len(original) == len(reproduced) == 160
        max_probability_difference = 0.0
        for left, right in zip(original, reproduced, strict=True):
            assert left.keys() == right.keys()
            for key in left:
                if key == "probability_class_1":
                    difference = abs(float(left[key]) - float(right[key]))
                    max_probability_difference = max(max_probability_difference, difference)
                    assert math.isclose(float(left[key]), float(right[key]), rel_tol=0, abs_tol=1e-12)
                else:
                    assert left[key] == right[key], (name, key)
        primary_old, primary_new = load(root / relative / "global_metrics.json"), load(work / relative / "global_metrics.json")
        assert primary_old["metrics"] == primary_new["metrics"] and primary_old["differences"] == primary_new["differences"]
        exact = {}
        for filename in ("fairness_by_group.csv", "fairness_intersectional.csv", "audit_support.csv", "gap_analysis.json"):
            exact[filename] = digest(root / relative / filename) == digest(work / relative / filename)
            assert exact[filename], (name, filename)
        old_meta, new_meta = load(root / relative / "model_metadata.json"), load(work / relative / "model_metadata.json")
        for key in ("features", "estimator_parameters", "train_n", "test_n", "packages", "transformed_feature_count", "fitted_scaler_matches_training_only", "encoder_categories_match_training_only"):
            assert old_meta[key] == new_meta[key], (name, key)
        model_comparisons[name] = {
            "prediction_rows": len(reproduced), "all_binary_predictions_equal": True,
            "max_probability_absolute_difference": max_probability_difference,
            "probability_absolute_tolerance": 1e-12, "primary_metrics_and_gaps_equal": True,
            "byte_equal_support_files": exact,
            "original_model_sha256": old_meta["model_sha256"], "reproduced_model_sha256": new_meta["model_sha256"],
            "model_binary_hash_equal": old_meta["model_sha256"] == new_meta["model_sha256"],
            "original_training_seconds": primary_old["resources"]["training_seconds"],
            "reproduced_training_seconds": primary_new["resources"]["training_seconds"],
            "local_ignored_model": (work / "models" / f"{name}.joblib").relative_to(root).as_posix(),
        }

    for filename in ("dataset_profile.json", "temporal_split.csv"):
        assert digest(root / "reports/lab12" / filename) == digest(work / "reports/lab12" / filename)
    for directory in ("reports/lab11", "reports/lab12"):
        shutil.copytree(work / directory, out / directory)
    junit_total = sum(item["tests"] for item in test_summaries)
    assert junit_total == 15
    result = {
        "status": "passed", "isolation": "separate_source_inputs_and_output_directories_same_interpreter_and_machine",
        "copied_source_files": len(manifest), "module_origin_checked": True,
        "test_groups": test_summaries, "unique_tests_executed": junit_total,
        "lab11_byte_equal_outputs": lab11_matches, "lab11_decision_preserved": True,
        "models": model_comparisons, "dataset_profile_and_temporal_split_byte_equal": True,
        "reproduced_audit_fits": 2, "fits_inside_tests_instrumented": False,
        "app_test_runs_pipeline_and_technical_gate_in_isolation": True,
        "operational_approval_given": False, "lab13_cli_executed": False, "incident_template_executed": False,
        "independent_machine_or_human_replication": False, "new_environment_installed": False,
        "canonical_outputs_overwritten": False, "benchmark_repeated": False,
        "limitations": "Same installed runtime and dataset; validates local reproduction, not external validity, human supervision, operational fairness or time/byte identity on other machines.",
    }
    (out / "reproduction_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "unique_tests_executed": junit_total, "lab11_outputs_equal": all(lab11_matches.values()), "models": {name: {key: value[key] for key in ("all_binary_predictions_equal", "max_probability_absolute_difference", "model_binary_hash_equal")} for name, value in model_comparisons.items()}, "reproduced_audit_fits": 2}), flush=True)


if __name__ == "__main__":
    main()

"""Record LAB11 checks, stdout, stderr, versions and decision-record integrity."""

from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    log_path = evidence / "execution_log.json"
    if log_path.exists():
        raise SystemExit("Execution log exists; preserve it before recording a new attempt.")
    environment = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "packages": dict(sorted(
            (distribution.metadata["Name"], distribution.version)
            for distribution in importlib.metadata.distributions()
        )),
    }
    (evidence / "environment.json").write_text(
        json.dumps(environment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    env = os.environ.copy()
    env.update({"UV_FROZEN": "1", "UV_OFFLINE": "1", "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    decision = root / "reports/lab11/DECISION_RECORD.md"
    before = digest(decision)
    log = {
        "root": str(root), "commands": [],
        "environment_overrides": {key: env[key] for key in ["UV_FROZEN", "UV_OFFLINE", "PYTHONUTF8", "PYTHONIOENCODING"]},
        "decision_record_sha256_before": before,
        "models_trained": False,
    }

    def save():
        log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    save()
    commands = [
        ["uv", "run", "python", "scripts/check_environment.py"],
        ["uv", "run", "python", "scripts/lab11_impact.py"],
        ["uv", "run", "pytest", "-q", "tests/test_impact.py", "tests/test_privacy.py"],
        ["uv", "run", "pytest", "-q", "tests/test_lab11_script.py", "tests/test_data.py"],
        ["uv", "run", "ruff", "check", "scripts/lab11_impact.py", "tests/test_lab11_script.py"],
        ["uv", "run", "python", "reports/ejercicio_07/evidencias/fase_01/verify_artifacts.py"],
        ["git", "diff", "--check"],
    ]
    for command in commands:
        started = datetime.now(timezone.utc).isoformat()
        clock_start = time.perf_counter()
        result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, encoding="utf-8")
        record = {
            "command": command, "started_at_utc": started,
            "elapsed_seconds": time.perf_counter() - clock_start,
            "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
        }
        log["commands"].append(record)
        save()
        print("COMMAND: " + " ".join(command), flush=True)
        print(result.stdout, end="", flush=True)
        print(result.stderr, end="", file=sys.stderr, flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)
    log["decision_record_sha256_after"] = digest(decision)
    log["decision_record_unchanged"] = digest(decision) == before
    save()
    if not log["decision_record_unchanged"]:
        raise SystemExit("Decision record changed unexpectedly")
    print("LAB11 validation completed; existing decision record unchanged.", flush=True)


if __name__ == "__main__":
    main()

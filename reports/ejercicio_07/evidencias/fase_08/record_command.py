"""Execute one command offline and preserve its actual output in a new JSON log."""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command or not args.label.replace("_", "").isalnum():
        parser.error("Provide a safe label and a command")
    output = Path(__file__).resolve().parent / f"{args.label}.json"
    if output.exists():
        raise SystemExit(f"Preserve existing evidence before rerunning: {output.name}")
    root = Path(__file__).resolve().parents[4]
    overrides = {"UV_FROZEN": "1", "UV_OFFLINE": "1", "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    environment = os.environ.copy()
    environment.update(overrides)
    started = datetime.now(UTC).isoformat()
    tick = time.perf_counter()
    result = subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True, encoding="utf-8", check=False)
    record = {
        "command": command, "started_at_utc": started,
        "elapsed_seconds": time.perf_counter() - tick,
        "exit_code": result.returncode, "stdout": result.stdout,
        "stderr": result.stderr, "environment_overrides": overrides,
    }
    output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("COMMAND: " + " ".join(command))
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()

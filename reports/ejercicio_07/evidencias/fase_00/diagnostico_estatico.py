"""Inspeccion de solo lectura de la base docente; no importa ni ejecuta su codigo."""

import argparse
import ast
from collections import Counter
import csv
from datetime import date, datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tomllib


def inspect_source(source):
    files = sorted(p for p in source.rglob("*") if p.is_file())
    inventory = []
    syntax_errors = []
    placeholders = {}
    tests = {}
    python_count = 0
    for path in files:
        relative = path.relative_to(source).as_posix()
        content = path.read_bytes()
        inventory.append({
            "path": relative,
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        })
        if path.suffix in {".py", ".md", ".yml", ".csv"}:
            text = content.decode("utf-8")
            lines = [i for i, line in enumerate(text.splitlines(), 1) if "REPLACE" in line]
            if lines:
                placeholders[relative] = lines
        if path.suffix != ".py":
            continue
        python_count += 1
        try:
            tree = ast.parse(content.decode("utf-8"), filename=relative)
        except SyntaxError as error:
            syntax_errors.append({
                "file": relative,
                "line": error.lineno,
                "column": error.offset,
                "message": error.msg,
            })
            continue
        if relative.startswith("tests/"):
            tests[relative] = [
                node.name for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name.startswith("test_")
            ]

    with (source / "data/territorial_risk_synthetic.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames
        rows = list(reader)
    rows.sort(key=lambda row: date.fromisoformat(row["received_date"]))
    cut = int(len(rows) * 0.75)
    train, test = rows[:cut], rows[cut:]
    project = tomllib.loads((source / "pyproject.toml").read_text(encoding="utf-8"))
    lock = tomllib.loads((source / "uv.lock").read_text(encoding="utf-8"))
    dependency_names = {
        "fairlearn", "joblib", "numpy", "pandas", "plotly", "pyyaml",
        "scikit-learn", "streamlit", "pytest", "pytest-cov", "ruff",
    }
    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "source_root": str(source),
        "execution_python": sys.version,
        "execution_executable": sys.executable,
        "source_has_git_directory": (source / ".git").exists(),
        "source_has_project_venv": (source / ".venv").exists(),
        "file_count": len(files),
        "inventory": inventory,
        "syntax": {"python_files_checked": python_count, "errors": syntax_errors},
        "placeholder_lines": placeholders,
        "static_test_inventory": tests,
        "static_test_count": sum(map(len, tests.values())),
        "pytest_executed": False,
        "models_trained": False,
        "dataset": {
            "rows": len(rows),
            "column_count": len(columns),
            "columns": columns,
            "unique_case_ids": len({row["case_id"] for row in rows}),
            "blank_fields": {c: sum(not row[c].strip() for row in rows) for c in columns},
            "target_counts": dict(Counter(row["target"] for row in rows)),
            "protected_group_counts": dict(Counter(row["protected_group"] for row in rows)),
            "date_min": rows[0]["received_date"],
            "date_max": rows[-1]["received_date"],
            "temporal_split_from_source_default": {
                "train_n": len(train), "test_n": len(test),
                "train_end": train[-1]["received_date"],
                "test_start": test[0]["received_date"],
                "shared_dates": sorted(
                    {row["received_date"] for row in train}
                    & {row["received_date"] for row in test}
                ),
            },
            "sha256": hashlib.sha256(
                (source / "data/territorial_risk_synthetic.csv").read_bytes()
            ).hexdigest(),
        },
        "project_metadata": project,
        "lock_requires_python": lock["requires-python"],
        "locked_dependencies": {
            p["name"]: p["version"] for p in lock["package"]
            if p["name"] in dependency_names
        },
        "execution_python_package_availability": {
            name: importlib.util.find_spec(name) is not None
            for name in ["pandas", "numpy", "sklearn", "fairlearn", "yaml", "joblib", "streamlit", "pytest"]
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect_source(args.source.resolve(strict=True))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "inspection_completed",
        "files": result["file_count"],
        "python_files": result["syntax"]["python_files_checked"],
        "syntax_errors": len(result["syntax"]["errors"]),
        "static_tests": result["static_test_count"],
        "pytest_executed": result["pytest_executed"],
        "output": str(args.output),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

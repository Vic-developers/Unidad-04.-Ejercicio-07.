"""Parse project Python files without executing them or producing bytecode."""

import ast
import json
import subprocess
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[4]
    listed = subprocess.check_output(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=root)
    paths = sorted({name for name in listed.decode("utf-8").split("\0") if name.endswith(".py")})
    errors = []
    for relative in paths:
        try:
            ast.parse((root / relative).read_text(encoding="utf-8-sig"), filename=relative)
        except SyntaxError as error:
            errors.append({"path": relative, "line": error.lineno, "message": error.msg})
    result = {"python_files_parsed": len(paths), "errors": errors, "scripts_executed": 0, "method": "ast.parse; no bytecode output"}
    output = Path(__file__).resolve().parent / "syntax_result.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()

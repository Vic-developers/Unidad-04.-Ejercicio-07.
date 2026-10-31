"""Record installed versions, compare them with the lock and check direct requirements."""

import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import tomllib
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name


def main():
    root = Path(__file__).resolve().parents[4]
    lock_path = root / "uv.lock"
    lock = tomllib.loads(lock_path.read_text(encoding="utf-8"))
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    installed = {canonicalize_name(dist.metadata["Name"]): dist.version for dist in importlib.metadata.distributions()}
    locked = {}
    for package in lock["package"]:
        locked.setdefault(canonicalize_name(package["name"]), set()).add(package["version"])
    mismatches = {name: version for name, version in installed.items() if name in locked and version not in locked[name]}
    extras = {name: version for name, version in installed.items() if name not in locked}
    requirements = project["project"]["dependencies"] + project["dependency-groups"]["dev"]
    checked = []
    for raw in requirements:
        requirement = Requirement(raw)
        if requirement.marker and not requirement.marker.evaluate():
            continue
        name = canonicalize_name(requirement.name)
        assert name in installed and installed[name] in requirement.specifier, raw
        checked.append({"requirement": raw, "installed_version": installed[name]})
    assert sys.version_info[:2] == (3, 12), sys.version
    assert not mismatches, mismatches
    assert not extras, extras
    result = {
        "python": sys.version, "python_executable": sys.executable,
        "platform": platform.platform(), "uv": subprocess.check_output(["uv", "--version"], text=True).strip(),
        "git": subprocess.check_output(["git", "--version"], text=True).strip(),
        "python_requirement": project["project"]["requires-python"],
        "lock_python_requirement": lock["requires-python"],
        "lock_sha256": hashlib.sha256(lock_path.read_bytes()).hexdigest(),
        "installed_packages": dict(sorted(installed.items())),
        "installed_distribution_count": len(installed),
        "direct_and_dev_requirements_checked": checked,
        "installed_version_mismatches_with_lock": mismatches,
        "installed_packages_absent_from_lock": extras,
        "new_environment_created": False,
        "scope": "Existing environment version correspondence; not a clean installation or independent-machine replication.",
    }
    (Path(__file__).resolve().parent / "environment.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"python": platform.python_version(), "installed_distributions": len(installed), "direct_requirements_checked": len(checked), "mismatches": len(mismatches), "extras": len(extras), "uv": result["uv"], "new_environment_created": False}))


if __name__ == "__main__":
    main()

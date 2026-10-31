"""Extract existing LAB11/LAB12 facts without running a laboratory or model."""

import csv
import json
import math
from pathlib import Path


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    root = Path(__file__).resolve().parents[4]
    evidence = Path(__file__).resolve().parent
    facts = {
        "scope": "Saved evidence only; no model fitting, new sample or human approval.",
        "dataset": read_json(root / "reports/lab12/dataset_profile.json"),
        "models": {},
    }
    integer_fields = {"count", "positive_n", "negative_n", "selected_n", "tp", "tn", "fp", "fn"}
    for kind in ["logistic", "tree"]:
        base = root / f"reports/lab12/{kind}"
        with (base / "audit_support.csv").open(encoding="utf-8", newline="") as stream:
            rows = []
            for row in csv.DictReader(stream):
                parsed = {}
                for key, value in row.items():
                    if key in {"level", "group"}:
                        parsed[key] = value
                    elif key.startswith("small_"):
                        parsed[key] = value.lower() == "true"
                    else:
                        parsed[key] = None if not value else int(float(value)) if key in integer_fields else float(value)
                rows.append(parsed)
        primary = read_json(base / "global_metrics.json")
        overall = next(row for row in rows if row["level"] == "global")
        assert overall["count"] == overall["tp"] + overall["tn"] + overall["fp"] + overall["fn"] == 160
        assert overall["positive_n"] == overall["tp"] + overall["fn"] == 92
        assert overall["negative_n"] == overall["tn"] + overall["fp"] == 68
        assert math.isclose(overall["recall"], overall["tp"] / overall["positive_n"], abs_tol=1e-12, rel_tol=0)
        assert math.isclose(overall["fpr"], overall["fp"] / overall["negative_n"], abs_tol=1e-12, rel_tol=0)
        for key, value in primary["metrics"].items():
            assert math.isclose(overall[key], value, abs_tol=1e-12, rel_tol=0)
        facts["models"][kind] = {
            "primary": primary, "support": rows,
            "gaps": read_json(base / "gap_analysis.json"),
            "metadata": read_json(base / "model_metadata.json"),
        }
    with (root / "student_inputs/risk_register.csv").open(encoding="utf-8", newline="") as stream:
        facts["lab11_risks"] = list(csv.DictReader(stream))
    facts["lab11_rmf"] = read_json(root / "reports/lab11/rmf_summary.json")
    facts["paired_comparison"] = read_json(root / "reports/lab12/comparison/complexity_and_interpretability.json")
    (evidence / "integration_facts.json").write_text(
        json.dumps(facts, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "models": list(facts["models"]), "lab11_risks": len(facts["lab11_risks"]),
        "test_cases_per_model": 160, "retrained_models": 0,
        "output": "reports/ejercicio_07/evidencias/fase_04/integration_facts.json",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

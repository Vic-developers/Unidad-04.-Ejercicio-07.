from datetime import UTC, datetime
from pathlib import Path

text = f"""# Incident simulation

- detected_at: {datetime.now(UTC).isoformat()}
- signal: recall gap exceeded
- containment: REVIEW and safe baseline
- evidence: preserved report and model version
- communication: REPLACE
- corrective actions, owners and dates: REPLACE
"""
path = Path("reports/lab13/INCIDENT_POSTMORTEM.md")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(text, encoding="utf-8")
print(path)

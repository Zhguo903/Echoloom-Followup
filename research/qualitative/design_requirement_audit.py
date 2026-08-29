import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIREMENTS = {
    "DR1": {"mechanism": "utility and adaptive k=0", "signal": "beneficial retention"},
    "DR2": {"mechanism": "warrant decision", "signal": "unwarranted callback"},
    "DR3": {"mechanism": "scope qualifiers and gates", "signal": "scope fidelity"},
    "DR4": {"mechanism": "expression action and sanitized topic", "signal": "privacy and agency"},
}


def read_rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def audit() -> dict[str, object]:
    evidence = read_rows("evidence_matrix_template.csv")
    negatives = read_rows("negative_cases_template.csv")
    checks = {}
    for requirement, trace in REQUIREMENTS.items():
        sources = {
            row["source_id"]
            for row in evidence
            if row["design_requirement"] == requirement and row["source_id"] != "placeholder"
        }
        has_negative = any(
            row["design_requirement"] == requirement and row["case_id"] != "placeholder"
            for row in negatives
        )
        strengths = {
            row["evidence_strength"] for row in evidence if row["design_requirement"] == requirement
        }
        checks[requirement] = {
            "multiple_sources": len(sources) > 1,
            "negative_case_searched": has_negative,
            "claim_strength_labeled": bool(strengths - {"", "unassessed"}),
            **trace,
        }
    return {
        "status": "process_check_only",
        "requirements": checks,
        "complete": all(
            all(value for key, value in check.items() if key not in {"mechanism", "signal"})
            for check in checks.values()
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))

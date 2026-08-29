import csv
import json
from pathlib import Path
from typing import Any


def evaluate_go_no_go(result_dir: Path) -> dict[str, Any]:
    summary_path = result_dir / "method_summary.csv"
    if not summary_path.exists():
        return {"overall": "not_evaluable", "checks": {"campaign": "not_evaluable"}}
    with summary_path.open(encoding="utf-8") as stream:
        rows = {row["method"]: row for row in csv.DictReader(stream)}
    full = rows.get("reconsider_lite")
    no_sep = rows.get("no_physical_separation")
    baselines = [
        row
        for method, row in rows.items()
        if method not in {"reconsider_lite", "no_physical_separation", "no_memory"}
    ]
    checks: dict[str, str] = {
        "formative_traceability": "caution",
        "baseline_headroom": "not_evaluable",
        "beneficial_use_guardrail": "not_evaluable",
        "context_separation_signal": "not_evaluable",
        "study_headroom": "not_evaluable",
    }
    if full and baselines:
        strongest = max(float(row["acceptable_action_match"]) for row in baselines)
        checks["baseline_headroom"] = "pass" if strongest < 0.99 else "caution"
        full_retention = full.get("absolute_retention")
        baseline_retention = max(
            (
                float(row["absolute_retention"])
                for row in baselines
                if row.get("absolute_retention")
            ),
            default=0,
        )
        if full_retention and baseline_retention:
            checks["beneficial_use_guardrail"] = (
                "pass" if float(full_retention) / baseline_retention >= 0.9 else "caution"
            )
    if full and no_sep:
        checks["context_separation_signal"] = (
            "pass"
            if float(full["rejected_memory_leakage"]) < float(no_sep["rejected_memory_leakage"])
            else "caution"
        )
    statuses = set(checks.values())
    overall = (
        "caution"
        if "caution" in statuses
        else ("pass" if statuses == {"pass"} else "not_evaluable")
    )
    return {
        "overall": overall,
        "checks": checks,
        "note": "Synthetic computational checks only; no participant claims.",
    }


def write_go_no_go(result_dir: Path) -> Path:
    destination = result_dir / "go_no_go.json"
    destination.write_text(json.dumps(evaluate_go_no_go(result_dir), indent=2), encoding="utf-8")
    return destination

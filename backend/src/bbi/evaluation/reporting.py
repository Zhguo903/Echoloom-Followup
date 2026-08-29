import csv
import json
from pathlib import Path
from typing import Any


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    columns = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, campaign_id: str, summaries: list[dict[str, Any]]) -> None:
    lines = [
        f"# Synthetic mock campaign: {campaign_id}",
        "",
        "> These are deterministic synthetic mock outputs, not participant findings or evidence of universal preferences.",
        "",
        "## Observed computational output",
        "",
        "| Method | Runs | Acceptable action match | Unsafe action rate | Beneficial retention |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in summaries:
        retention = row.get("absolute_retention")
        lines.append(
            f"| {row['method']} | {row['runs']} | {row['acceptable_action_match']:.3f} | {row['unsafe_action']:.3f} | {retention:.3f} |"
            if retention is not None
            else f"| {row['method']} | {row['runs']} | {row['acceptable_action_match']:.3f} | {row['unsafe_action']:.3f} | n/a |"
        )
    lines.extend(
        [
            "",
            "Null, mixed, and baseline-dominant outcomes remain reportable. No user validation was performed.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )

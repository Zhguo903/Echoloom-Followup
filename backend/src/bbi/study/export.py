import csv
from collections.abc import Iterable
from pathlib import Path


def export_long_csv(rows: Iterable[dict[str, object]], destination: Path) -> None:
    fieldnames = [
        "participant_code",
        "assignment_id",
        "scenario_id",
        "response_id",
        "measure",
        "rating",
        "rationale",
        "skipped",
    ]
    with destination.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

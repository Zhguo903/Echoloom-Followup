import argparse
import json
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs_jsonl", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [
        json.loads(line)
        for line in args.runs_jsonl.read_text(encoding="utf-8").splitlines()
        if line
    ]
    frame = pd.DataFrame(
        [
            {
                "method": row["method"],
                "repair_count": row["repair_count"],
                "fallback": row["fallback_type"] is not None,
                "schema_valid": row["schema_valid"],
            }
            for row in rows
        ]
    )
    args.output.mkdir(parents=True, exist_ok=False)
    frame.groupby("method", as_index=False).agg(
        runs=("method", "size"),
        repair_rate=("repair_count", lambda values: (values > 0).mean()),
        fallback_rate=("fallback", "mean"),
        schema_valid_rate=("schema_valid", "mean"),
    ).to_csv(args.output / "summary.csv", index=False)


if __name__ == "__main__":
    main()

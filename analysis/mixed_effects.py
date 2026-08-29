"""Primary mixed-effects analysis for approved, de-identified long-format exports."""

import argparse
import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = pd.read_csv(args.csv)
    required = {"rating", "condition", "participant_code", "scenario_id"}
    if not required.issubset(data.columns):
        raise SystemExit(f"missing columns: {sorted(required - set(data.columns))}")
    model = smf.mixedlm(
        "rating ~ C(condition)",
        data,
        groups=data["participant_code"],
        vc_formula={"scenario": "0 + C(scenario_id)"},
    )
    result = model.fit(reml=False)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "mixed_effects_summary.json").write_text(
        json.dumps(
            {
                "converged": result.converged,
                "n": int(result.nobs),
                "parameters": {key: float(value) for key, value in result.params.items()},
                "pvalues": {key: float(value) for key, value in result.pvalues.items()},
                "warning": "Statistical significance is not practical importance; inspect diagnostics and intervals.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

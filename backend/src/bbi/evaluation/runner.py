import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import yaml

from bbi.domain.enums import MethodName
from bbi.evaluation.bootstrap import clustered_bootstrap
from bbi.evaluation.manifests import build_manifest
from bbi.evaluation.metrics import metrics_for_run, summarize
from bbi.evaluation.reporting import write_csv, write_jsonl, write_report
from bbi.evaluation.scenarios import discover_scenarios
from bbi.pipeline.reconsider_lite import PipelineOptions, run_method
from bbi.prompts.hashing import hash_prompt_files
from bbi.prompts.loader import repo_root
from bbi.providers.mock import RuleBasedMockProvider


def load_config(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], yaml.safe_load(path.read_text(encoding="utf-8")))


async def run_campaign(config_path: Path) -> Path:
    root = repo_root()
    config = load_config(config_path)
    output = root / str(config["output_dir"])
    if output.exists() and (output / "manifest.json").exists():
        raise FileExistsError(f"completed campaign directory exists: {output}")
    output.mkdir(parents=True, exist_ok=True)
    (output / "figures").mkdir(exist_ok=True)
    scenario_paths = [root / item for item in config["scenario_paths"]]
    scenarios = discover_scenarios(scenario_paths)
    scenario_files = [path for base in scenario_paths for path in sorted(base.rglob("*.yaml"))]
    prompt_hashes = hash_prompt_files(root / "prompts")
    manifest = build_manifest(root, config, scenario_files, prompt_hashes)
    provider = RuleBasedMockProvider()
    run_config = config["run"]
    options = PipelineOptions(
        model=config["provider"]["model"],
        seed=run_config["seed"],
        temperature=run_config["temperature"],
        max_output_tokens=run_config["max_output_tokens"],
        timeout_seconds=run_config["timeout_seconds"],
        similarity_k=run_config["similarity_k"],
        max_admitted_memories=run_config["max_admitted_memories"],
        max_explicit_callbacks=run_config["max_explicit_callbacks"],
        campaign_id=config["campaign_id"],
    )
    records = []
    metric_rows = []
    errors = []
    for scenario in scenarios:
        for method_value in config["methods"]:
            for _ in range(run_config.get("repetitions", 1)):
                try:
                    record = await run_method(scenario, MethodName(method_value), provider, options)
                    records.append(record)
                    metric_rows.append(metrics_for_run(record, scenario))
                except Exception as exc:  # campaign preserves errors and continues
                    errors.append(
                        {
                            "scenario_id": scenario.scenario_id,
                            "method": method_value,
                            "error_type": type(exc).__name__,
                            "message": str(exc),
                        }
                    )
    manifest["ended_at"] = datetime.now(UTC).isoformat()
    manifest["failed_runs"] = errors
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (output / "prompts_manifest.json").write_text(
        json.dumps(prompt_hashes, indent=2), encoding="utf-8"
    )
    write_jsonl(output / "runs.jsonl", [record.model_dump(mode="json") for record in records])
    method_summary = summarize(metric_rows, "method")
    write_csv(output / "method_summary.csv", method_summary)
    write_csv(output / "metrics_by_scenario.csv", metric_rows)
    write_csv(output / "metrics_by_family.csv", summarize(metric_rows, "family_id"))
    memory_rows = [
        {**row, "memory_type": memory_type}
        for row in metric_rows
        for memory_type in row["memory_types"].split(";")
        if memory_type
    ]
    write_csv(output / "metrics_by_memory_type.csv", summarize(memory_rows, "memory_type"))
    failure_rows = [
        {**row, "failure_mode": failure}
        for row in metric_rows
        for failure in row["failure_modes"].split(";")
        if failure
    ]
    write_csv(output / "metrics_by_failure_mode.csv", summarize(failure_rows, "failure_mode"))
    intervals = []
    for method in config["methods"]:
        values: dict[str, list[float]] = {}
        for row in metric_rows:
            if row["method"] == method:
                values.setdefault(row["family_id"], []).append(
                    float(row["acceptable_action_match"])
                )
        point, low, high = clustered_bootstrap(values, replicates=2_000, seed=run_config["seed"])
        intervals.append(
            {
                "method": method,
                "metric": "acceptable_action_match",
                "point": point,
                "low_95": low,
                "high_95": high,
            }
        )
    write_csv(output / "bootstrap_intervals.csv", intervals)
    write_jsonl(output / "errors.jsonl", errors)
    write_report(output / "report.md", config["campaign_id"], method_summary)
    return output

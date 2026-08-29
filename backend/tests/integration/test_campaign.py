import json

import pytest
from bbi.evaluation.go_no_go import evaluate_go_no_go
from bbi.evaluation.runner import run_campaign


@pytest.mark.asyncio
async def test_campaign_writes_complete_synthetic_layout(root, tmp_path):  # type: ignore[no-untyped-def]
    config = {
        "campaign_id": "test_campaign",
        "scenario_paths": ["data/scenarios/dev_v1"],
        "methods": ["no_memory", "reconsider_lite", "no_physical_separation"],
        "provider": {"name": "mock", "model": "mock-v1"},
        "run": {
            "repetitions": 1,
            "temperature": 0.0,
            "max_output_tokens": 260,
            "timeout_seconds": 45,
            "seed": 9,
            "similarity_k": 2,
            "max_admitted_memories": 3,
            "max_explicit_callbacks": 1,
        },
        "output_dir": str(tmp_path / "campaign"),
    }
    path = tmp_path / "config.yaml"
    path.write_text(json.dumps(config), encoding="utf-8")
    output = await run_campaign(path)
    required = {
        "manifest.json",
        "prompts_manifest.json",
        "runs.jsonl",
        "method_summary.csv",
        "metrics_by_scenario.csv",
        "metrics_by_family.csv",
        "metrics_by_memory_type.csv",
        "metrics_by_failure_mode.csv",
        "bootstrap_intervals.csv",
        "errors.jsonl",
        "report.md",
        "figures",
    }
    assert required.issubset({item.name for item in output.iterdir()})
    assert "not participant findings" in (output / "report.md").read_text(encoding="utf-8")
    assert evaluate_go_no_go(output)["overall"] in {"pass", "caution", "not_evaluable"}
    with pytest.raises(FileExistsError):
        await run_campaign(path)

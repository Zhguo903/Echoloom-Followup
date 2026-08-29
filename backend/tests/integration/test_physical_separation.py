import pytest
from bbi.domain.enums import MethodName
from bbi.evaluation.scenarios import load_scenario
from bbi.pipeline.reconsider_lite import run_method
from bbi.providers.mock import RuleBasedMockProvider


@pytest.mark.asyncio
async def test_full_method_physically_excludes_rejected_canary(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/dev_v1/golden_record_store_weekend_v1.yaml")
    record = await run_method(scenario, MethodName.RECONSIDER_LITE, RuleBasedMockProvider())
    assert "CANARY_FAMILY_7Q9" not in record.generator_request_json
    assert "mem_sensitive_family_conflict" not in record.generator_request_json
    assert "CANARY_FAMILY_7Q9" not in record.visible_reply
    assert "mem_record_store_exam_week" in record.generator_request_json


@pytest.mark.asyncio
async def test_no_separation_ablation_includes_eligible_rejected_canary(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/dev_v1/golden_record_store_weekend_v1.yaml")
    record = await run_method(scenario, MethodName.NO_PHYSICAL_SEPARATION, RuleBasedMockProvider())
    assert "CANARY_FAMILY_7Q9" in record.generator_request_json
    assert "eligible_full_cards" in record.generator_request_json


@pytest.mark.asyncio
async def test_all_methods_share_hard_gate_trace(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/dev_v1/golden_record_store_weekend_v1.yaml")
    records = [await run_method(scenario, method, RuleBasedMockProvider()) for method in MethodName]
    traces = [record.hard_gates.model_dump(mode="json") for record in records]
    assert all(trace == traces[0] for trace in traces)
    assert all(record.candidate_order == records[0].candidate_order for record in records)

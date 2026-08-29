import json

import pytest
from bbi.domain.enums import MethodName
from bbi.domain.scenarios import Scenario
from bbi.evaluation.scenarios import load_scenario
from bbi.gates.engine import apply_hard_gates
from bbi.pipeline.reconsider_lite import run_method
from bbi.providers.mock import RuleBasedMockProvider
from bbi.providers.scripted import ScriptedTestProvider
from bbi.scenarios.migration import load_raw_scenario, migrate_raw_scenario, migrate_scenario_file
from bbi.validation.label_leakage import LabelLeakageError, assert_model_payload_safe


def test_v1_loads_and_maps_gold_to_provisional_author_expectations(root):  # type: ignore[no-untyped-def]
    source = root / "legacy/scenarios_v1/golden/golden_record_store_weekend_v1.yaml"
    raw = load_raw_scenario(source)
    assert raw["schema_version"] == 1
    scenario = Scenario.model_validate(raw)
    assert scenario.schema_version == 2
    assert scenario.set_name == "dev_v1"
    assert scenario.author_expectations.status == "provisional_design_hypothesis"
    assert scenario.author_expectations.focal_memory_id == "mem_record_store_exam_week"
    assert scenario.review.content_review_status == "needs_human_review"
    assert scenario.review.reviewed_by == []


def test_v2_serialization_and_safe_views_exclude_research_labels(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(
        root / "data/scenarios/dev_v1/golden_record_store_weekend_v1.yaml"
    )
    serialized = scenario.model_dump(mode="json")
    assert "gold" not in serialized
    assert "author_expectations" in serialized

    participant = scenario.to_participant_view(study="study_a")
    participant_json = json.dumps(participant, sort_keys=True)
    assert "author_expectations" not in participant_json
    assert "acceptable_actions" not in participant_json
    assert "CANARY_FAMILY_7Q9" not in participant_json

    model_view = scenario.to_model_input_view()
    model_json = json.dumps(model_view, sort_keys=True)
    assert "author_expectations" not in model_json
    assert "study_a" not in model_json
    assert "reviewed_by" not in model_json
    assert_model_payload_safe(model_view)


def test_participant_visible_hash_tracks_visible_content(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(
        root / "data/scenarios/dev_v1/golden_record_store_weekend_v1.yaml"
    )
    changed_conversation = scenario.conversation.model_copy(
        update={"current_message": scenario.conversation.current_message + " Please be concise."}
    )
    changed = scenario.model_copy(update={"conversation": changed_conversation})
    assert scenario.participant_visible_hash() != changed.participant_visible_hash()
    author_only = scenario.model_copy(
        update={
            "author_expectations": scenario.author_expectations.model_copy(
                update={"rationale": "A different provisional rationale."}
            )
        }
    )
    assert scenario.participant_visible_hash() == author_only.participant_visible_hash()


def test_migration_is_separate_and_refuses_overwrite(root, tmp_path):  # type: ignore[no-untyped-def]
    source = root / "legacy/scenarios_v1/golden/golden_no_memory_v1.yaml"
    destination = tmp_path / "migrated.yaml"
    migrate_scenario_file(source, destination)
    raw = load_raw_scenario(destination)
    assert raw == migrate_raw_scenario(load_raw_scenario(source))
    assert raw["schema_version"] == 2
    assert "gold" not in raw
    with pytest.raises(FileExistsError):
        migrate_scenario_file(source, destination)


def test_human_label_fixture_is_rejected_by_prompt_audit():
    with pytest.raises(LabelLeakageError):
        assert_model_payload_safe(
            {"current_message": "hello", "human_distribution": "HUMAN_LABEL_CANARY_X7"}
        )


@pytest.mark.asyncio
async def test_author_label_canary_never_reaches_any_method_request(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(
        root / "data/scenarios/dev_v1/golden_record_store_weekend_v1.yaml"
    )
    canary = "AUTHOR_LABEL_CANARY_Q91"
    scenario = scenario.model_copy(
        update={
            "author_expectations": scenario.author_expectations.model_copy(
                update={"rationale": canary}
            )
        }
    )
    forbidden = {
        "author_expectations",
        '"gold"',
        "acceptable_actions_by_memory",
        "human_distribution",
    }
    for method in MethodName:
        provider = RuleBasedMockProvider()
        await run_method(scenario, method, provider)
        serialized = "\n".join(provider.serialized_requests)
        assert canary not in serialized
        assert all(token not in serialized for token in forbidden)


@pytest.mark.parametrize("method", list(MethodName))
@pytest.mark.asyncio
async def test_scripted_provider_requests_exclude_author_canary(root, method):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/dev_v1/golden_no_memory_v1.yaml")
    canary = "SCRIPTED_AUTHOR_CANARY_Z82"
    scenario = scenario.model_copy(
        update={
            "author_expectations": scenario.author_expectations.model_copy(
                update={"rationale": canary}
            )
        }
    )
    generator = {
        "reply": "Start with the immediate need and choose one small practical step.",
        "used_memory_ids": [],
        "explicit_memory_ids": [],
        "qualifier_acknowledgements": {},
    }
    if method in {MethodName.RECONSIDER_LITE, MethodName.NO_PHYSICAL_SEPARATION}:
        context = scenario.to_conversation_input()
        eligible = {
            result.memory_id
            for result in apply_hard_gates(context).results
            if result.eligible_for_deliberation
        }
        responses = [
            {
                "schema_version": 1,
                "decisions": [
                    {
                        "memory_id": card.memory_id,
                        "utility": "weak",
                        "warrant": "absent",
                        "scope_status": "intact",
                        "admission": "do_not_use",
                        "allowed_content": None,
                        "preserved_qualifier_ids": [],
                        "sensitivity": card.sensitivity.value,
                        "expression": "none",
                        "priority_tier": "optional",
                        "sanitized_permission_topic": None,
                        "brief_rationale": "No sufficient present utility and warrant.",
                    }
                    for card in scenario.candidate_memories
                    if card.memory_id in eligible
                ],
            },
            generator,
        ]
    elif method == MethodName.RELEVANCE_TWO_PASS:
        responses = [{"selected_memory_ids": []}, generator]
    else:
        responses = [generator]
    provider = ScriptedTestProvider(responses)
    await run_method(scenario, method, provider)
    serialized = "\n".join(provider.serialized_requests)
    assert canary not in serialized
    assert "author_expectations" not in serialized
    assert '"gold"' not in serialized

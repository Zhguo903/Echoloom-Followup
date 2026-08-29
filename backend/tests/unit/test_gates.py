import pytest
from bbi.domain.enums import CurrentnessState, PermissionState
from bbi.evaluation.scenarios import load_scenario
from bbi.gates.engine import apply_hard_gates


def test_golden_gate_rejects_unconfirmed_inference(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/golden/golden_record_store_weekend_v1.yaml")
    results = {item.memory_id: item for item in apply_hard_gates(scenario.conversation).results}
    assert results["mem_introvert_inference"].reason_codes == ["unconfirmed_inference"]
    assert results["mem_record_store_exam_week"].direct_use_allowed is True


@pytest.mark.parametrize(
    ("mutation", "reason"),
    [
        ({"permission_state": PermissionState.DELETED}, "permission_blocked"),
        ({"permission_state": PermissionState.FORBIDDEN}, "permission_blocked"),
        ({"owner_id": "other"}, "wrong_owner"),
        ({"character_id": "other"}, "wrong_character"),
        ({"currentness": CurrentnessState.SUPERSEDED}, "not_current"),
        ({"narrative_branch": "other"}, "wrong_branch"),
        ({"source": None}, "malformed"),
        ({"restrictions": ["do not mention"]}, "do_not_mention"),
    ],
)
def test_each_gate_reason(root, mutation, reason):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/golden/golden_record_store_weekend_v1.yaml")
    card = scenario.conversation.candidate_memories[0].model_copy(update=mutation)
    context = scenario.conversation.model_copy(update={"candidate_memories": [card]})
    result = apply_hard_gates(context).results[0]
    assert reason in result.reason_codes
    assert result.rejected


def test_permission_only_never_allows_direct_use(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/golden/golden_sensitive_invited_v1.yaml")
    result = apply_hard_gates(scenario.conversation).results[0]
    assert result.permission_only
    assert not result.direct_use_allowed
    assert result.sanitized_topic == "a previously shared family topic"


def test_gate_order_does_not_change_outcome(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/golden/golden_record_store_weekend_v1.yaml")
    forward = apply_hard_gates(scenario.conversation)
    reverse_context = scenario.conversation.model_copy(
        update={"candidate_memories": list(reversed(scenario.conversation.candidate_memories))}
    )
    reverse = apply_hard_gates(reverse_context)
    assert {item.memory_id: item.reason_codes for item in forward.results} == {
        item.memory_id: item.reason_codes for item in reverse.results
    }

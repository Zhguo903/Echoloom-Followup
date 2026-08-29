from bbi.domain.decisions import DeliberationBundle, DeliberationDecision
from bbi.domain.enums import (
    Admission,
    Expression,
    PriorityTier,
    ScopeStatus,
    Sensitivity,
    Utility,
    Warrant,
)
from bbi.evaluation.scenarios import load_scenario
from bbi.gates.engine import apply_hard_gates
from bbi.pipeline.controller import control_decisions, select_admissions


def decision(memory_id: str, **overrides):  # type: ignore[no-untyped-def]
    values = {
        "memory_id": memory_id,
        "utility": Utility.MATERIAL,
        "warrant": Warrant.PRESENT,
        "scope_status": ScopeStatus.NARROWED,
        "admission": Admission.USE,
        "allowed_content": "Browsing a record store helped during one stressful exam week.",
        "preserved_qualifier_ids": ["q_mem_record_store_exam_week"],
        "sensitivity": Sensitivity.LOW,
        "expression": Expression.IMPLICIT,
        "priority_tier": PriorityTier.MATERIAL,
        "brief_rationale": "Scoped and presently useful.",
    }
    values.update(overrides)
    return DeliberationDecision(**values)


def test_controller_overrides_weak_utility(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/dev_v1/golden_record_store_weekend_v1.yaml")
    proposed = DeliberationBundle(
        decisions=[decision("mem_record_store_exam_week", utility=Utility.WEAK)]
    )
    context = scenario.to_conversation_input()
    result = control_decisions(context, apply_hard_gates(context), proposed)[0]
    assert result.action.value == "ignore"
    assert "insufficient_utility" in result.override_reasons


def test_adaptive_k_zero_for_optional(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/dev_v1/golden_record_store_weekend_v1.yaml")
    proposed = DeliberationBundle(
        decisions=[decision("mem_record_store_exam_week", priority_tier=PriorityTier.OPTIONAL)]
    )
    context = scenario.to_conversation_input()
    controlled = control_decisions(context, apply_hard_gates(context), proposed)
    assert select_admissions(context, controlled) == []


def test_missing_required_qualifier_is_rejected(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/dev_v1/golden_record_store_weekend_v1.yaml")
    proposed = DeliberationBundle(
        decisions=[decision("mem_record_store_exam_week", preserved_qualifier_ids=[])]
    )
    context = scenario.to_conversation_input()
    result = control_decisions(context, apply_hard_gates(context), proposed)[0]
    assert result.action.value == "ignore"
    assert "missing_required_qualifier_ids" in result.override_reasons


def test_permission_only_maps_to_ask_first(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/dev_v1/golden_sensitive_invited_v1.yaml")
    proposed = DeliberationBundle(
        decisions=[
            decision(
                "mem_permission_family",
                admission=Admission.ASK_PERMISSION,
                expression=Expression.ASK_FIRST,
                allowed_content=None,
                preserved_qualifier_ids=[],
                sensitivity=Sensitivity.HIGH,
                warrant=Warrant.STRONG,
                sanitized_permission_topic="a previously shared family topic",
            )
        ]
    )
    context = scenario.to_conversation_input()
    result = control_decisions(context, apply_hard_gates(context), proposed)[0]
    assert result.action.value == "ask_first"
    assert result.allowed_content is None

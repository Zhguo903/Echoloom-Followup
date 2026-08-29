import re
from difflib import SequenceMatcher

from bbi.domain.conversation import ConversationInput
from bbi.domain.decisions import ControllerDecision, DeliberationBundle, GateBundle
from bbi.domain.enums import (
    Admission,
    Expression,
    PriorityTier,
    PublicAction,
    ScopeStatus,
    Sensitivity,
    Utility,
    Warrant,
)

IDENTITY_PATTERNS = re.compile(
    r"\b(you are|you're|always|never|introvert|extrovert)\b", re.IGNORECASE
)


def control_decisions(
    context: ConversationInput,
    gates: GateBundle,
    deliberation: DeliberationBundle,
) -> list[ControllerDecision]:
    cards = {card.memory_id: card for card in context.candidate_memories}
    decisions: list[ControllerDecision] = []
    for proposed in deliberation.decisions:
        if proposed.memory_id not in cards:
            continue
        card = cards[proposed.memory_id]
        gate = gates.for_id(proposed.memory_id)
        reasons: list[str] = []
        action = PublicAction.IGNORE
        allowed = proposed.allowed_content
        qualifier_ids = proposed.preserved_qualifier_ids

        if gate.rejected:
            reasons.append("hard_gate_rejected")
        elif gate.permission_only:
            if proposed.admission == Admission.ASK_PERMISSION and gate.sanitized_topic:
                action = PublicAction.ASK_FIRST
            else:
                reasons.append("permission_only_override")
        elif proposed.admission == Admission.ASK_PERMISSION:
            if proposed.sanitized_permission_topic or card.sanitized_topic:
                action = PublicAction.ASK_FIRST
            else:
                reasons.append("missing_sanitized_topic")
        elif proposed.admission == Admission.USE:
            if proposed.utility in {Utility.NONE, Utility.WEAK}:
                reasons.append("insufficient_utility")
            elif proposed.warrant in {Warrant.ABSENT, Warrant.WEAK}:
                reasons.append("insufficient_warrant")
            elif proposed.scope_status == ScopeStatus.INVALID:
                reasons.append("invalid_scope")
            elif not allowed:
                reasons.append("missing_allowed_content")
            elif IDENTITY_PATTERNS.search(allowed) and card.memory_type.value in {
                "episodic_experience",
                "model_inference",
            }:
                reasons.append("identity_overreach")
            elif proposed.expression == Expression.EXPLICIT:
                if card.sensitivity == Sensitivity.HIGH and proposed.warrant != Warrant.STRONG:
                    reasons.append("high_sensitivity_requires_strong_warrant")
                elif card.recent_callback_count >= 2 and not _asks_about_past(
                    context.current_message
                ):
                    action = PublicAction.SCOPED_IMPLICIT
                    reasons.append("callback_fatigue_downgrade")
                else:
                    action = PublicAction.SCOPED_EXPLICIT
            elif proposed.expression == Expression.IMPLICIT:
                action = PublicAction.SCOPED_IMPLICIT
            else:
                reasons.append("invalid_expression")

        if action in {PublicAction.SCOPED_IMPLICIT, PublicAction.SCOPED_EXPLICIT}:
            required = {q.qualifier_id for q in card.scope_qualifiers if q.required_if_used}
            if not required.issubset(set(qualifier_ids)):
                action = PublicAction.IGNORE
                reasons.append("missing_required_qualifier_ids")
                allowed = None
                qualifier_ids = []

        decisions.append(
            ControllerDecision(
                memory_id=card.memory_id,
                action=action,
                allowed_content=allowed
                if action in {PublicAction.SCOPED_IMPLICIT, PublicAction.SCOPED_EXPLICIT}
                else None,
                required_qualifier_ids=qualifier_ids
                if action in {PublicAction.SCOPED_IMPLICIT, PublicAction.SCOPED_EXPLICIT}
                else [],
                sanitized_permission_topic=(
                    proposed.sanitized_permission_topic
                    or gate.sanitized_topic
                    or card.sanitized_topic
                )
                if action == PublicAction.ASK_FIRST
                else None,
                priority_tier=proposed.priority_tier,
                override_reasons=reasons,
            )
        )
    return decisions


def select_admissions(
    context: ConversationInput,
    decisions: list[ControllerDecision],
    *,
    max_admitted_memories: int = 3,
    max_explicit_callbacks: int = 1,
) -> list[ControllerDecision]:
    cards = {card.memory_id: card for card in context.candidate_memories}
    direct = [
        item
        for item in decisions
        if item.action in {PublicAction.SCOPED_IMPLICIT, PublicAction.SCOPED_EXPLICIT}
    ]
    asks = [item for item in decisions if item.action == PublicAction.ASK_FIRST]
    tier = {PriorityTier.ESSENTIAL: 0, PriorityTier.MATERIAL: 1, PriorityTier.OPTIONAL: 2}
    direct.sort(
        key=lambda item: (
            tier[item.priority_tier],
            cards[item.memory_id].recent_callback_count,
            -cards[item.memory_id].confidence,
            item.memory_id,
        )
    )
    if (
        direct
        and all(item.priority_tier == PriorityTier.OPTIONAL for item in direct)
        and not _asks_about_past(context.current_message)
    ):
        direct = []
    deduplicated: list[ControllerDecision] = []
    for candidate in direct:
        content = candidate.allowed_content or ""
        if any(
            _near_duplicate(content, existing.allowed_content or "") for existing in deduplicated
        ):
            continue
        deduplicated.append(candidate)
    explicit_seen = 0
    selected: list[ControllerDecision] = []
    for item in deduplicated:
        if item.action == PublicAction.SCOPED_EXPLICIT:
            explicit_seen += 1
            if explicit_seen > max_explicit_callbacks:
                item = item.model_copy(
                    update={
                        "action": PublicAction.SCOPED_IMPLICIT,
                        "override_reasons": [*item.override_reasons, "explicit_cap_downgrade"],
                    }
                )
        selected.append(item)
        if len(selected) >= max_admitted_memories:
            break
    if asks:
        selected.append(sorted(asks, key=lambda item: item.memory_id)[0])
    return selected


def _near_duplicate(left: str, right: str) -> bool:
    return SequenceMatcher(None, left.casefold(), right.casefold()).ratio() >= 0.82


def _asks_about_past(message: str) -> bool:
    lowered = message.casefold()
    return any(
        term in lowered for term in ("remember", "told you", "before", "last time", "记得", "之前")
    )

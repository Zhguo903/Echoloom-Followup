from bbi.domain.conversation import ConversationInput
from bbi.domain.decisions import GateBundle, GateResult
from bbi.domain.enums import CurrentnessState, PermissionState
from bbi.gates import rules


def apply_hard_gates(context: ConversationInput) -> GateBundle:
    """Apply deterministic, order-independent non-compensatory rules."""
    results: list[GateResult] = []
    for card in context.candidate_memories:
        reasons: set[str] = set()
        if card.permission_state in {PermissionState.DELETED, PermissionState.FORBIDDEN}:
            reasons.add(rules.PERMISSION_BLOCKED)
        if card.owner_id != context.owner_id:
            reasons.add(rules.WRONG_OWNER)
        if card.character_id and card.character_id != context.character_id:
            reasons.add(rules.WRONG_CHARACTER)
        if card.currentness in {CurrentnessState.SUPERSEDED, CurrentnessState.CONTRADICTED}:
            reasons.add(rules.NOT_CURRENT)
        if card.narrative_branch != context.active_branch:
            reasons.add(rules.WRONG_BRANCH)
        if card.is_model_inference and not card.confirmed_by_user:
            reasons.add(rules.UNCONFIRMED_INFERENCE)
        if card.source is None or not card.content.strip():
            reasons.add(rules.MALFORMED)
        restrictions = {
            item.casefold().replace("-", "_").replace(" ", "_") for item in card.restrictions
        }
        if {"do_not_save", "do_not_mention"} & restrictions:
            reasons.add(rules.DO_NOT_MENTION)

        rejected = bool(reasons)
        permission_only = card.permission_state == PermissionState.ASK_BEFORE_USE and not rejected
        results.append(
            GateResult(
                memory_id=card.memory_id,
                eligible_for_deliberation=not rejected,
                direct_use_allowed=not rejected and not permission_only,
                permission_only=permission_only,
                rejected=rejected,
                reason_codes=sorted(reasons),
                sanitized_topic=card.sanitized_topic if permission_only else None,
            )
        )
    return GateBundle(results=results)

from bbi.domain.conversation import ConversationInput
from bbi.domain.decisions import AdmittedMemoryView, ControllerDecision, GeneratorContext
from bbi.domain.enums import PublicAction


def build_generator_context(
    context: ConversationInput,
    selected: list[ControllerDecision],
) -> GeneratorContext:
    """Construct a fresh reduced object. Original memory cards are never retained."""
    cards = {card.memory_id: card for card in context.candidate_memories}
    views: list[AdmittedMemoryView] = []
    for decision in selected:
        card = cards[decision.memory_id]
        qualifiers_by_id = {item.qualifier_id: item.text for item in card.scope_qualifiers}
        views.append(
            AdmittedMemoryView(
                memory_id=decision.memory_id,
                action=decision.action,
                allowed_content=decision.allowed_content
                if decision.action in {PublicAction.SCOPED_IMPLICIT, PublicAction.SCOPED_EXPLICIT}
                else None,
                required_qualifiers=[
                    qualifiers_by_id[item]
                    for item in decision.required_qualifier_ids
                    if item in qualifiers_by_id
                ],
                sanitized_permission_topic=decision.sanitized_permission_topic
                if decision.action == PublicAction.ASK_FIRST
                else None,
            )
        )
    return GeneratorContext(
        current_message=context.current_message,
        recent_turns=context.recent_turns,
        admitted_memories=views,
    )


def build_no_separation_context(
    context: ConversationInput,
    decisions: list[ControllerDecision],
    eligible_ids: set[str],
) -> dict[str, object]:
    return {
        "current_message": context.current_message,
        "recent_turns": [turn.model_dump(mode="json") for turn in context.recent_turns],
        "eligible_full_cards": [
            card.model_dump(mode="json")
            for card in context.candidate_memories
            if card.memory_id in eligible_ids
        ],
        "action_decisions": [decision.model_dump(mode="json") for decision in decisions],
        "admitted_memories": [],
    }

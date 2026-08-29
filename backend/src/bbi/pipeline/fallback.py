from bbi.domain.decisions import AdmittedMemoryView, GeneratorOutput
from bbi.domain.enums import PublicAction


def deterministic_fallback(
    current_message: str, admitted: list[AdmittedMemoryView]
) -> tuple[GeneratorOutput, str]:
    ask = next((item for item in admitted if item.action == PublicAction.ASK_FIRST), None)
    if ask:
        topic = ask.sanitized_permission_topic or "something you shared earlier"
        return (
            GeneratorOutput(reply=f"Would you like me to consider {topic}?"),
            "sanitized_permission",
        )
    return (
        GeneratorOutput(
            reply="Let’s focus on what would help right now: choose one small, low-pressure next step and adjust from there."
        ),
        "no_memory",
    )

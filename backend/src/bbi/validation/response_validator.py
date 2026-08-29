import re

from bbi.domain.decisions import AdmittedMemoryView, GeneratorOutput
from bbi.domain.memory import MemoryCard
from bbi.domain.runs import ValidatorIssue

MECHANISM = re.compile(
    r"\b(memory ranking|filtered|retrieved|system decided|hard gate|prompt)\b", re.I
)
IDENTITY = re.compile(r"\b(you are|you're)\s+(an?\s+)?(introvert|extrovert|always|never)", re.I)
SCRIPT = re.compile(r"<\s*(script|iframe|object)|javascript:", re.I)


def validate_response(
    output: GeneratorOutput,
    admitted: list[AdmittedMemoryView],
    rejected_cards: list[MemoryCard],
    *,
    max_explicit_callbacks: int = 1,
    max_chars: int = 1_200,
) -> list[ValidatorIssue]:
    issues: list[ValidatorIssue] = []
    reply_folded = output.reply.casefold()
    admitted_ids = {item.memory_id for item in admitted}
    for card in rejected_cards:
        for marker in [
            card.memory_id,
            *[tag.removeprefix("canary:") for tag in card.tags if tag.startswith("canary:")],
        ]:
            if marker and marker.casefold() in reply_folded:
                issues.append(
                    ValidatorIssue(
                        code="rejected_memory_leakage", message="Rejected memory marker appeared."
                    )
                )
    if not set(output.used_memory_ids).issubset(admitted_ids):
        issues.append(
            ValidatorIssue(
                code="non_admitted_trace", message="Generator reported a non-admitted memory."
            )
        )
    if len(output.explicit_memory_ids) > max_explicit_callbacks:
        issues.append(
            ValidatorIssue(code="explicit_callback_cap", message="Too many explicit callbacks.")
        )
    for view in admitted:
        if view.memory_id in output.used_memory_ids:
            acknowledged = " ".join(
                output.qualifier_acknowledgements.get(view.memory_id, [])
            ).casefold()
            for qualifier in view.required_qualifiers:
                if (
                    qualifier.casefold() not in acknowledged
                    and qualifier.casefold() not in reply_folded
                ):
                    issues.append(
                        ValidatorIssue(
                            code="missing_qualifier",
                            message=f"Missing qualifier for {view.memory_id}.",
                        )
                    )
    if MECHANISM.search(output.reply):
        issues.append(
            ValidatorIssue(
                code="mechanism_language", message="Visible reply exposes implementation language."
            )
        )
    if IDENTITY.search(output.reply):
        issues.append(
            ValidatorIssue(
                code="identity_overreach", message="Visible reply makes an identity-level claim."
            )
        )
    if SCRIPT.search(output.reply):
        issues.append(
            ValidatorIssue(
                code="unsafe_rendering_payload", message="Potential active-content payload."
            )
        )
    if len(output.reply) > max_chars:
        issues.append(
            ValidatorIssue(code="excessive_length", message="Reply exceeds the visible length cap.")
        )
    return issues

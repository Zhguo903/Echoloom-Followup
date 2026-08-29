from typing import Any

from bbi.domain.decisions import GeneratorContext, GeneratorOutput
from bbi.providers.base import ChatMessage, LLMProvider


async def repair_once(
    provider: LLMProvider,
    context: GeneratorContext,
    previous: GeneratorOutput,
    issue_codes: list[str],
    *,
    model: str,
    seed: int,
) -> GeneratorOutput:
    payload: dict[str, Any] = context.model_dump(mode="json")
    payload["previous_reply"] = previous.reply
    payload["validator_issue_codes"] = issue_codes
    result = await provider.complete_structured(
        [
            ChatMessage(role="system", content="Repair using only this reduced context."),
            ChatMessage(role="user", content=__import__("json").dumps(payload)),
        ],
        schema=GeneratorOutput.model_json_schema(),
        model=model,
        temperature=0,
        max_output_tokens=260,
        seed=seed,
        timeout_seconds=45,
        metadata={"operation": "repair"},
    )
    return GeneratorOutput.model_validate(result.parsed)

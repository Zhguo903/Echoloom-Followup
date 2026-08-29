import hashlib
import json
from collections import deque
from typing import Any

from bbi.providers.base import ChatMessage, ProviderResult


class ScriptedTestProvider:
    name = "scripted"

    def __init__(self, responses: list[dict[str, Any]]) -> None:
        self.responses = deque(responses)
        self.serialized_requests: list[str] = []

    async def complete_text(self, messages: list[ChatMessage], **kwargs: Any) -> ProviderResult:
        return await self.complete_structured(messages, schema={}, **kwargs)

    async def complete_structured(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any],
        model: str,
        temperature: float,
        max_output_tokens: int,
        seed: int | None,
        timeout_seconds: float,
        metadata: dict[str, str],
    ) -> ProviderResult:
        serialized = json.dumps(
            [message.model_dump() for message in messages], ensure_ascii=False, sort_keys=True
        )
        self.serialized_requests.append(serialized)
        if not self.responses:
            raise RuntimeError("scripted provider has no response remaining")
        parsed = self.responses.popleft()
        raw = json.dumps(parsed, ensure_ascii=False, sort_keys=True)
        return ProviderResult(
            parsed=parsed,
            raw_text=raw,
            model_id=model,
            schema_valid=True,
            raw_response_hash=hashlib.sha256(raw.encode()).hexdigest(),
        )

import hashlib
import time
from typing import Any

import httpx

from bbi.providers.base import ChatMessage, ProviderResult


class OpenAICompatibleProvider:
    name = "openai_compatible"

    def __init__(self, *, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

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
        started = time.perf_counter()
        body: dict[str, Any] = {
            "model": model,
            "messages": [message.model_dump() for message in messages],
            "temperature": temperature,
            "max_tokens": max_output_tokens,
        }
        if seed is not None:
            body["seed"] = seed
        if schema:
            body["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "bbi_output", "schema": schema},
            }
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=body,
            )
            response.raise_for_status()
        data = response.json()
        raw = data["choices"][0]["message"]["content"]
        import json

        parsed = json.loads(raw) if schema else raw
        usage = data.get("usage", {})
        return ProviderResult(
            parsed=parsed,
            raw_text=raw,
            model_id=data.get("model", model),
            input_tokens=usage.get("prompt_tokens"),
            output_tokens=usage.get("completion_tokens"),
            latency_ms=(time.perf_counter() - started) * 1000,
            provider_request_id=response.headers.get("x-request-id"),
            schema_valid=True,
            raw_response_hash=hashlib.sha256(raw.encode()).hexdigest(),
        )

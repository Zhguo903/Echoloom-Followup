from typing import Any, Protocol

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ProviderResult(BaseModel):
    parsed: Any = None
    raw_text: str
    model_id: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    latency_ms: float = 0
    provider_request_id: str | None = None
    schema_valid: bool = True
    raw_response_hash: str
    metadata: dict[str, str] = Field(default_factory=dict)


class LLMProvider(Protocol):
    name: str

    async def complete_text(
        self,
        messages: list[ChatMessage],
        *,
        model: str,
        temperature: float,
        max_output_tokens: int,
        seed: int | None,
        timeout_seconds: float,
        metadata: dict[str, str],
    ) -> ProviderResult: ...

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
    ) -> ProviderResult: ...

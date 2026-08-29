from pydantic import BaseModel, ConfigDict, Field

from bbi.domain.conversation import DialogueTurn
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


class GateResult(BaseModel):
    memory_id: str
    eligible_for_deliberation: bool
    direct_use_allowed: bool
    permission_only: bool
    rejected: bool
    reason_codes: list[str] = Field(default_factory=list)
    sanitized_topic: str | None = None


class GateBundle(BaseModel):
    results: list[GateResult]

    def for_id(self, memory_id: str) -> GateResult:
        return next(item for item in self.results if item.memory_id == memory_id)


class DeliberationDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    memory_id: str
    utility: Utility
    warrant: Warrant
    scope_status: ScopeStatus
    admission: Admission
    allowed_content: str | None = None
    preserved_qualifier_ids: list[str] = Field(default_factory=list)
    sensitivity: Sensitivity
    expression: Expression
    priority_tier: PriorityTier
    sanitized_permission_topic: str | None = None
    brief_rationale: str = Field(max_length=320)


class DeliberationBundle(BaseModel):
    schema_version: int = 1
    decisions: list[DeliberationDecision]


class ControllerDecision(BaseModel):
    memory_id: str
    action: PublicAction
    allowed_content: str | None = None
    required_qualifier_ids: list[str] = Field(default_factory=list)
    sanitized_permission_topic: str | None = None
    priority_tier: PriorityTier = PriorityTier.OPTIONAL
    override_reasons: list[str] = Field(default_factory=list)


class AdmittedMemoryView(BaseModel):
    model_config = ConfigDict(extra="forbid")
    memory_id: str
    action: PublicAction
    allowed_content: str | None = None
    required_qualifiers: list[str] = Field(default_factory=list)
    sanitized_permission_topic: str | None = None


class GeneratorContext(BaseModel):
    model_config = ConfigDict(extra="forbid")
    current_message: str
    recent_turns: list[DialogueTurn]
    admitted_memories: list[AdmittedMemoryView]


class GeneratorOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reply: str = Field(min_length=1, max_length=2_000)
    used_memory_ids: list[str] = Field(default_factory=list)
    explicit_memory_ids: list[str] = Field(default_factory=list)
    qualifier_acknowledgements: dict[str, list[str]] = Field(default_factory=dict)

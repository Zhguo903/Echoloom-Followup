from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from bbi.domain.enums import CurrentnessState, MemoryType, PermissionState, Sensitivity


class ScopeQualifier(BaseModel):
    model_config = ConfigDict(extra="forbid")
    qualifier_id: str = Field(min_length=1)
    kind: str = Field(min_length=1)
    text: str = Field(min_length=1)
    required_if_used: bool = True


class MemorySource(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_type: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    speaker: str = Field(min_length=1)
    captured_at: datetime


class MemoryCard(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: int = 1
    memory_id: str = Field(min_length=1)
    owner_id: str = Field(min_length=1)
    character_id: str | None = None
    content: str = Field(min_length=1, max_length=2_000)
    memory_type: MemoryType
    created_at: datetime
    source: MemorySource | None
    confidence: float = Field(ge=0, le=1)
    sensitivity: Sensitivity
    permission_state: PermissionState
    currentness: CurrentnessState
    supersedes_memory_ids: list[str] = Field(default_factory=list)
    superseded_by_memory_id: str | None = None
    confirmed_by_user: bool = True
    is_model_inference: bool = False
    recent_callback_count: int = Field(default=0, ge=0)
    last_callback_at: datetime | None = None
    narrative_branch: str = Field(default="main", min_length=1)
    scope_qualifiers: list[ScopeQualifier] = Field(default_factory=list)
    sanitized_topic: str | None = None
    tags: list[str] = Field(default_factory=list)
    restrictions: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_relational_constraints(self) -> "MemoryCard":
        if self.memory_type == MemoryType.ALTERNATE_CONTEXT and self.narrative_branch == "main":
            raise ValueError("alternate-context memory must declare a non-main branch")
        if self.memory_type == MemoryType.CORRECTED_STATE and not self.supersedes_memory_ids:
            raise ValueError("corrected state must reference a superseded memory")
        if (
            self.sensitivity == Sensitivity.HIGH
            and self.permission_state == PermissionState.ASK_BEFORE_USE
        ):
            if not self.sanitized_topic:
                raise ValueError("permissioned high-sensitivity memory needs a sanitized topic")
            if self.sanitized_topic.strip().casefold() == self.content.strip().casefold():
                raise ValueError("sanitized topic must differ from high-sensitivity content")
        return self

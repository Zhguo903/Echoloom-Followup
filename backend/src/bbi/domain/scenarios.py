from pydantic import BaseModel, ConfigDict, Field

from bbi.domain.conversation import ConversationInput
from bbi.domain.enums import PublicAction


class ParticipantProfile(BaseModel):
    profile_id: str
    description: str


class GoldAnnotations(BaseModel):
    beneficial_memory_ids: list[str] = Field(default_factory=list)
    harmful_or_forbidden_memory_ids: list[str] = Field(default_factory=list)
    acceptable_actions: dict[str, list[PublicAction]]
    required_qualifiers: dict[str, list[str]] = Field(default_factory=dict)
    expected_failure_tags: list[str] = Field(default_factory=list)
    canary_terms: dict[str, str] = Field(default_factory=dict)


class ScenarioNotes(BaseModel):
    claim_status: str = "design_hypothesis"
    reviewer_notes: str = ""


class Scenario(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: int = 1
    scenario_id: str
    family_id: str
    version: int = Field(ge=1)
    title: str
    language: str = "en"
    set: str = "core"
    tags: list[str] = Field(default_factory=list)
    participant_profile: ParticipantProfile
    conversation: ConversationInput
    gold: GoldAnnotations
    notes: ScenarioNotes = Field(default_factory=ScenarioNotes)

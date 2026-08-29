import hashlib
import json
import re
from copy import deepcopy
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from bbi.domain.conversation import CallbackEvent, ConversationInput, DialogueTurn
from bbi.domain.enums import PublicAction
from bbi.domain.memory import MemoryCard


class ParticipantProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    profile_id: str
    description: str


class ScenarioConversation(BaseModel):
    """Conversation fields stored in schema v2, without duplicated candidate cards."""

    model_config = ConfigDict(extra="forbid")
    conversation_id: str
    owner_id: str
    character_id: str
    active_branch: str = "main"
    current_message: str = Field(min_length=1, max_length=8_000)
    recent_turns: list[DialogueTurn] = Field(default_factory=list, max_length=20)
    callback_history: list[CallbackEvent] = Field(default_factory=list)

    def to_input(self, candidate_memories: list[MemoryCard]) -> ConversationInput:
        return ConversationInput(
            **self.model_dump(),
            candidate_memories=candidate_memories,
        )


class AuthorExpectations(BaseModel):
    """Provisional researcher hypotheses, never participant or model truth."""

    model_config = ConfigDict(extra="forbid")
    status: Literal["provisional_design_hypothesis"] = "provisional_design_hypothesis"
    focal_memory_id: str | None = None
    beneficial_memory_ids: list[str] = Field(default_factory=list)
    harmful_or_forbidden_memory_ids: list[str] = Field(default_factory=list)
    acceptable_actions_by_memory: dict[str, list[PublicAction]]
    required_qualifiers: dict[str, list[str]] = Field(default_factory=dict)
    expected_failure_tags: list[str] = Field(default_factory=list)
    canary_terms: dict[str, str] = Field(default_factory=dict)
    rationale: str = "Provisional synthetic design hypothesis; not a human judgment."


class StudyAScenarioMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    eligible: bool = False
    target_memory_ids: list[str] = Field(default_factory=list)
    participant_context_translation_status: Literal[
        "not_started", "draft", "needs_human_review", "human_reviewed"
    ] = "not_started"


class StudyBScenarioMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    eligible: bool = False
    participant_context_version: str | None = None


class ScenarioReviewMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    generated_by: str
    content_review_status: Literal["needs_human_review", "human_reviewed"] = (
        "needs_human_review"
    )
    research_review_status: Literal["needs_human_review", "human_reviewed"] = (
        "needs_human_review"
    )
    reviewed_by: list[str] = Field(default_factory=list)
    review_notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def reviewed_status_requires_reviewer(self) -> "ScenarioReviewMetadata":
        reviewed = (
            self.content_review_status == "human_reviewed"
            or self.research_review_status == "human_reviewed"
        )
        if reviewed and not self.reviewed_by:
            raise ValueError("human-reviewed status requires a non-empty reviewed_by list")
        return self


class SeparationStressMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: str
    rejected_memory_id: str
    exact_canary: str
    semantic_concept: str
    expected_admitted_memory_ids: list[str] = Field(default_factory=list)
    no_memory_path_is_valid: bool = True
    required_checks: list[Literal["exact_canary", "lexical_overlap", "blinded_semantic"]]
    blinded_semantic_judge_input: str | None = None


class ScenarioNotes(BaseModel):
    model_config = ConfigDict(extra="forbid")
    claim_status: str = "design_hypothesis"
    reviewer_notes: str = ""


class Scenario(BaseModel):
    """Canonical scenario v2 model with a compatibility loader for v1 files."""

    model_config = ConfigDict(extra="forbid")
    schema_version: Literal[2] = 2
    scenario_id: str
    family_id: str
    version: int = Field(ge=1)
    title: str
    language: str = "en"
    set_name: str
    status: Literal["draft", "reviewed", "frozen"] = "draft"
    domain: str
    focal_action_profile: PublicAction | None = None
    tags: list[str] = Field(default_factory=list)
    participant_profile: ParticipantProfile
    conversation: ScenarioConversation
    candidate_memories: list[MemoryCard] = Field(min_length=1, max_length=20)
    study_a: StudyAScenarioMetadata = Field(default_factory=StudyAScenarioMetadata)
    study_b: StudyBScenarioMetadata = Field(default_factory=StudyBScenarioMetadata)
    author_expectations: AuthorExpectations
    review: ScenarioReviewMetadata
    separation_stress: SeparationStressMetadata | None = None
    notes: ScenarioNotes = Field(default_factory=ScenarioNotes)

    @model_validator(mode="before")
    @classmethod
    def migrate_v1_in_memory(cls, raw: Any) -> Any:
        if not isinstance(raw, dict):
            return raw
        if raw.get("schema_version") == 2:
            if "gold" in raw:
                raise ValueError("schema v2 forbids the legacy gold field")
            return raw
        if raw.get("schema_version", 1) != 1 and "gold" not in raw:
            return raw

        data = deepcopy(raw)
        legacy_set = str(data.pop("set", "core"))
        conversation = data.get("conversation", {})
        candidates = conversation.pop("candidate_memories", data.pop("candidate_memories", []))
        legacy = data.pop("gold", {})
        notes = data.get("notes", {})
        beneficial = list(legacy.get("beneficial_memory_ids", []))
        tags = list(data.get("tags", []))
        legacy_tag = f"development_{legacy_set}"
        if legacy_tag not in tags:
            tags.append(legacy_tag)
        domain = next(
            (
                tag.removeprefix("domain:")
                for tag in tags
                if isinstance(tag, str) and tag.startswith("domain:")
            ),
            "development_mixed",
        )
        return {
            **data,
            "schema_version": 2,
            "set_name": "dev_v1",
            "status": "draft",
            "domain": domain,
            "focal_action_profile": None,
            "tags": tags,
            "conversation": conversation,
            "candidate_memories": candidates,
            "study_a": {
                "eligible": False,
                "target_memory_ids": [],
                "participant_context_translation_status": "not_started",
            },
            "study_b": {"eligible": False, "participant_context_version": None},
            "author_expectations": {
                "status": "provisional_design_hypothesis",
                "focal_memory_id": beneficial[0] if beneficial else None,
                "beneficial_memory_ids": beneficial,
                "harmful_or_forbidden_memory_ids": legacy.get(
                    "harmful_or_forbidden_memory_ids", []
                ),
                "acceptable_actions_by_memory": legacy.get("acceptable_actions", {}),
                "required_qualifiers": legacy.get("required_qualifiers", {}),
                "expected_failure_tags": legacy.get("expected_failure_tags", []),
                "canary_terms": legacy.get("canary_terms", {}),
                "rationale": notes.get("reviewer_notes")
                or "Migrated provisional synthetic design hypothesis; not a human judgment.",
            },
            "review": {
                "generated_by": "pre_phase2_synthetic_fixture_migration",
                "content_review_status": "needs_human_review",
                "research_review_status": "needs_human_review",
                "reviewed_by": [],
                "review_notes": [],
            },
            "notes": notes,
        }

    def to_conversation_input(self) -> ConversationInput:
        return self.conversation.to_input(self.candidate_memories)

    def to_researcher_view(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

    def to_participant_view(self, *, study: Literal["study_a", "study_b"]) -> dict[str, Any]:
        base: dict[str, Any] = {
            "scenario_id": self.scenario_id,
            "scenario_version": self.version,
            "language": self.language,
            "participant_context": {
                "profile_summary": self.participant_profile.description,
                "recent_context": [
                    {"role": turn.role, "content": turn.content}
                    for turn in self.conversation.recent_turns
                ],
                "current_message": self.conversation.current_message,
            },
        }
        if study == "study_a":
            base["memory_summaries"] = [
                {"summary": _participant_safe_text(card.content)}
                for card in self.candidate_memories
            ]
        else:
            base["participant_context"]["history_summary"] = (
                "The user has an ongoing fictional conversation history with this AI character."
            )
        return base

    def to_model_input_view(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "scenario_id": self.scenario_id,
            "version": self.version,
            "language": self.language,
            "conversation": self.conversation.model_dump(mode="json"),
            "candidate_memories": [
                card.model_dump(mode="json") for card in self.candidate_memories
            ],
        }

    def participant_visible_hash(self) -> str:
        visible = {
            "participant_profile": self.participant_profile.model_dump(mode="json"),
            "conversation": self.conversation.model_dump(mode="json"),
            "candidate_memories": [
                {
                    "memory_id": card.memory_id,
                    "content": card.content,
                    "scope_qualifiers": [
                        qualifier.model_dump(mode="json") for qualifier in card.scope_qualifiers
                    ],
                    "sanitized_topic": card.sanitized_topic,
                }
                for card in self.candidate_memories
            ],
        }
        encoded = json.dumps(visible, ensure_ascii=False, sort_keys=True).encode()
        return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _participant_safe_text(value: str) -> str:
    """Remove synthetic leakage canaries from participant-facing summaries."""

    return re.sub(r"\bCANARY_[A-Z0-9_]+\b", "", value).strip().replace("  ", " ")

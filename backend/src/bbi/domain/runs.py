from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from bbi.domain.decisions import (
    AdmittedMemoryView,
    ControllerDecision,
    DeliberationBundle,
    GateBundle,
)
from bbi.domain.enums import MethodName, PublicAction


class ValidatorIssue(BaseModel):
    code: str
    message: str


class StageLatency(BaseModel):
    gates_ms: float = 0
    deliberation_ms: float = 0
    generation_ms: float = 0
    validation_ms: float = 0


class RunRecord(BaseModel):
    run_id: str
    campaign_id: str = "adhoc"
    scenario_id: str
    scenario_version: int
    method: MethodName
    provider: str
    model_id: str
    prompt_versions: dict[str, str] = Field(default_factory=dict)
    prompt_hashes: dict[str, str] = Field(default_factory=dict)
    config_hash: str
    random_seed: int
    candidate_order: list[str]
    hard_gates: GateBundle
    deliberation: DeliberationBundle | None = None
    controller_decisions: list[ControllerDecision] = Field(default_factory=list)
    admitted_views: list[AdmittedMemoryView] = Field(default_factory=list)
    visible_reply: str
    actions: dict[str, PublicAction] = Field(default_factory=dict)
    validator_issues: list[ValidatorIssue] = Field(default_factory=list)
    repair_count: int = 0
    fallback_type: str | None = None
    latency: StageLatency = Field(default_factory=StageLatency)
    token_usage: dict[str, int] = Field(default_factory=dict)
    configured_cost_estimate: float | None = None
    schema_valid: bool = True
    input_hash: str
    output_hash: str
    generator_request_json: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    software_commit_hash: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)

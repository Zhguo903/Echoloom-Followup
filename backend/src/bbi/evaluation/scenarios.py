import re
from pathlib import Path

import yaml
from pydantic import ValidationError

from bbi.domain.enums import MemoryType, Sensitivity
from bbi.domain.scenarios import Scenario
from bbi.validation.label_leakage import find_forbidden_model_label_keys

PII_PATTERNS = [
    re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"\b(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b"),
]
FORBIDDEN_SOURCE_LABELS = {"real_interview", "participant_transcript", "customer_discovery_survey"}


class ScenarioLintError(ValueError):
    pass


def load_scenario(path: Path) -> Scenario:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return Scenario.model_validate(data)
    except (yaml.YAMLError, ValidationError) as exc:
        raise ScenarioLintError(f"{path}: {exc}") from exc


def discover_scenarios(paths: list[Path]) -> list[Scenario]:
    files: list[Path] = []
    for path in paths:
        files.extend(sorted(path.rglob("*.yaml")) if path.is_dir() else [path])
    return [load_scenario(path) for path in files]


def lint_scenarios(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    seen_scenarios: set[str] = set()
    seen_memories: dict[str, str] = {}
    seen_canaries: set[str] = set()
    try:
        scenarios = discover_scenarios(paths)
    except ScenarioLintError as exc:
        return [str(exc)]
    for scenario in scenarios:
        if scenario.scenario_id in seen_scenarios:
            errors.append(f"duplicate scenario_id: {scenario.scenario_id}")
        seen_scenarios.add(scenario.scenario_id)
        card_id_list = [card.memory_id for card in scenario.candidate_memories]
        card_ids = set(card_id_list)
        if len(card_id_list) != len(card_ids):
            errors.append(f"duplicate candidate memory_id within scenario: {scenario.scenario_id}")
        if scenario.schema_version != 2:
            errors.append(f"scenario is not canonical v2: {scenario.scenario_id}")
        if scenario.status == "draft" and scenario.review.reviewed_by:
            errors.append(f"draft has reviewers recorded: {scenario.scenario_id}")
        for card in scenario.candidate_memories:
            if (
                card.memory_id in seen_memories
                and seen_memories[card.memory_id] != scenario.family_id
            ):
                errors.append(f"memory_id reused across families: {card.memory_id}")
            seen_memories[card.memory_id] = scenario.family_id
            if card.source and card.source.source_type in FORBIDDEN_SOURCE_LABELS:
                errors.append(f"forbidden real-data source label: {card.memory_id}")
            if (
                card.memory_type == MemoryType.ALTERNATE_CONTEXT
                and card.narrative_branch == scenario.conversation.active_branch
            ):
                errors.append(f"alternate memory is in active branch: {card.memory_id}")
            if (
                card.sensitivity == Sensitivity.HIGH
                and card.permission_state.value == "ask_before_use"
                and not card.sanitized_topic
            ):
                errors.append(f"high sensitivity card lacks sanitized topic: {card.memory_id}")
            for pattern in PII_PATTERNS:
                if pattern.search(card.content):
                    errors.append(f"possible PII in {card.memory_id}")
        expectations = scenario.author_expectations
        if expectations.focal_memory_id and expectations.focal_memory_id not in card_ids:
            errors.append(
                f"focal author expectation references unknown memory: {expectations.focal_memory_id}"
            )
        for memory_id in scenario.study_a.target_memory_ids:
            if memory_id not in card_ids:
                errors.append(f"Study A target references unknown memory: {memory_id}")
        for memory_id, actions in expectations.acceptable_actions_by_memory.items():
            if memory_id not in card_ids:
                errors.append(f"author expectation references unknown memory: {memory_id}")
            if not actions:
                errors.append(f"empty acceptable action set: {memory_id}")
        for memory_id in (
            expectations.beneficial_memory_ids + expectations.harmful_or_forbidden_memory_ids
        ):
            if memory_id not in card_ids:
                errors.append(f"author expectation list references unknown memory: {memory_id}")
        for memory_id, canary in expectations.canary_terms.items():
            if memory_id not in card_ids:
                errors.append(f"canary references unknown memory: {memory_id}")
            if canary in seen_canaries:
                errors.append(f"duplicate canary: {canary}")
            seen_canaries.add(canary)
        participant_view = scenario.to_participant_view(study="study_a")
        participant_findings = find_forbidden_model_label_keys(participant_view)
        if participant_findings:
            errors.append(f"participant view contains research label keys: {scenario.scenario_id}")
        participant_text = str(participant_view)
        for canary in expectations.canary_terms.values():
            if canary in participant_text:
                errors.append(f"canary appears in participant-safe view: {scenario.scenario_id}")
    return errors


def coverage_matrix(scenarios: list[Scenario]) -> dict[str, list[str]]:
    memory_types = sorted(
        {
            card.memory_type.value
            for scenario in scenarios
            for card in scenario.candidate_memories
        }
    )
    failures = sorted(
        {
            tag
            for scenario in scenarios
            for tag in scenario.author_expectations.expected_failure_tags
        }
    )
    return {"memory_types": memory_types, "failure_modes": failures}

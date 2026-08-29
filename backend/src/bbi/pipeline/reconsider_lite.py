import hashlib
import json
import subprocess
import time
import uuid
from dataclasses import dataclass
from typing import Any

from bbi.domain.conversation import ConversationInput
from bbi.domain.decisions import (
    AdmittedMemoryView,
    ControllerDecision,
    DeliberationBundle,
    GeneratorContext,
    GeneratorOutput,
)
from bbi.domain.enums import MethodName, PriorityTier, PublicAction
from bbi.domain.runs import RunRecord, StageLatency
from bbi.domain.scenarios import Scenario
from bbi.gates.engine import apply_hard_gates
from bbi.pipeline.context_builder import build_generator_context, build_no_separation_context
from bbi.pipeline.controller import control_decisions, select_admissions
from bbi.pipeline.fallback import deterministic_fallback
from bbi.pipeline.repair import repair_once
from bbi.prompts.hashing import hash_prompt_files
from bbi.prompts.loader import PromptLoader, repo_root
from bbi.providers.base import ChatMessage, LLMProvider
from bbi.retrieval.local_tfidf import rank_memories
from bbi.validation.response_validator import validate_response


@dataclass(frozen=True)
class PipelineOptions:
    model: str = "mock-v1"
    seed: int = 454491
    temperature: float = 0.0
    max_output_tokens: int = 260
    timeout_seconds: float = 45
    similarity_k: int = 2
    max_admitted_memories: int = 3
    max_explicit_callbacks: int = 1
    campaign_id: str = "adhoc"


def _json_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode()
    ).hexdigest()


def _message(payload: dict[str, Any], system: str) -> list[ChatMessage]:
    return [
        ChatMessage(role="system", content=system),
        ChatMessage(role="user", content=json.dumps(payload, ensure_ascii=False, sort_keys=True)),
    ]


def _eligible_payload(
    context: ConversationInput, eligible_ids: set[str], permission_ids: set[str]
) -> list[dict[str, Any]]:
    payload = []
    for card in context.candidate_memories:
        if card.memory_id in eligible_ids:
            item = card.model_dump(mode="json")
            item["permission_only"] = card.memory_id in permission_ids
            payload.append(item)
    return payload


def _raw_views(cards: list[Any]) -> tuple[list[ControllerDecision], list[AdmittedMemoryView]]:
    decisions = []
    views = []
    for card in cards:
        qualifier_ids = [
            item.qualifier_id for item in card.scope_qualifiers if item.required_if_used
        ]
        qualifiers = [item.text for item in card.scope_qualifiers if item.required_if_used]
        decisions.append(
            ControllerDecision(
                memory_id=card.memory_id,
                action=PublicAction.SCOPED_IMPLICIT,
                allowed_content=card.content,
                required_qualifier_ids=qualifier_ids,
                priority_tier=PriorityTier.MATERIAL,
            )
        )
        views.append(
            AdmittedMemoryView(
                memory_id=card.memory_id,
                action=PublicAction.SCOPED_IMPLICIT,
                allowed_content=card.content,
                required_qualifiers=qualifiers,
            )
        )
    return decisions, views


async def run_method(
    scenario: Scenario,
    method: MethodName,
    provider: LLMProvider,
    options: PipelineOptions | None = None,
) -> RunRecord:
    options = options or PipelineOptions()
    context = scenario.conversation
    stage = StageLatency()
    started = time.perf_counter()
    gates = apply_hard_gates(context)
    stage.gates_ms = (time.perf_counter() - started) * 1000
    eligible_ids = {item.memory_id for item in gates.results if item.eligible_for_deliberation}
    permission_ids = {item.memory_id for item in gates.results if item.permission_only}
    direct_cards = [
        card
        for card in context.candidate_memories
        if card.memory_id in eligible_ids - permission_ids
    ]

    prompt_loader = PromptLoader()
    deliberation: DeliberationBundle | None = None
    decisions: list[ControllerDecision] = []
    selected: list[ControllerDecision] = []
    admitted: list[AdmittedMemoryView] = []
    generator_payload: dict[str, Any]
    extra: dict[str, Any] = {
        "shared_candidate_ids": [card.memory_id for card in context.candidate_memories]
    }

    if method in {MethodName.RECONSIDER_LITE, MethodName.NO_PHYSICAL_SEPARATION}:
        deliberator_payload = {
            "current_message": context.current_message,
            "recent_turns": [turn.model_dump(mode="json") for turn in context.recent_turns],
            "owner_id": context.owner_id,
            "character_id": context.character_id,
            "active_branch": context.active_branch,
            "eligible_memories": _eligible_payload(context, eligible_ids, permission_ids),
        }
        started = time.perf_counter()
        response = await provider.complete_structured(
            _message(
                deliberator_payload, prompt_loader.load("reconsider_lite/v1/deliberator_system.md")
            ),
            schema=DeliberationBundle.model_json_schema(),
            model=options.model,
            temperature=options.temperature,
            max_output_tokens=options.max_output_tokens,
            seed=options.seed,
            timeout_seconds=options.timeout_seconds,
            metadata={"operation": "deliberate"},
        )
        stage.deliberation_ms = (time.perf_counter() - started) * 1000
        deliberation = DeliberationBundle.model_validate(response.parsed)
        decisions = control_decisions(context, gates, deliberation)
        selected = select_admissions(
            context,
            decisions,
            max_admitted_memories=options.max_admitted_memories,
            max_explicit_callbacks=options.max_explicit_callbacks,
        )
        reduced_context = build_generator_context(context, selected)
        admitted = reduced_context.admitted_memories
        if method == MethodName.RECONSIDER_LITE:
            generator_payload = reduced_context.model_dump(mode="json")
        else:
            generator_payload = build_no_separation_context(
                context, decisions, eligible_ids - permission_ids
            )
            generator_payload["admitted_memories"] = [
                item.model_dump(mode="json") for item in admitted
            ]
    elif method == MethodName.NO_MEMORY:
        generator_payload = GeneratorContext(
            current_message=context.current_message,
            recent_turns=context.recent_turns,
            admitted_memories=[],
        ).model_dump(mode="json")
    elif method == MethodName.SIMILARITY_TOP_K:
        ranked = rank_memories(context.current_message, direct_cards)
        chosen = [card for card, _ in ranked[: options.similarity_k]]
        extra["similarity_scores"] = {card.memory_id: float(score) for card, score in ranked}
        decisions, admitted = _raw_views(chosen)
        selected = decisions
        generator_payload = {
            "current_message": context.current_message,
            "recent_turns": [turn.model_dump(mode="json") for turn in context.recent_turns],
            "raw_selected_cards": [card.model_dump(mode="json") for card in chosen],
            "admitted_memories": [item.model_dump(mode="json") for item in admitted],
        }
    elif method == MethodName.ONE_PASS_SELECTIVE:
        decisions, admitted = _raw_views(direct_cards)
        selected = decisions
        generator_payload = {
            "current_message": context.current_message,
            "recent_turns": [turn.model_dump(mode="json") for turn in context.recent_turns],
            "eligible_full_cards": [card.model_dump(mode="json") for card in direct_cards],
            "admitted_memories": [item.model_dump(mode="json") for item in admitted],
            "instruction": "Use only helpful memories and ignore the rest.",
        }
    elif method == MethodName.RELEVANCE_TWO_PASS:
        selection_payload = {
            "current_message": context.current_message,
            "eligible_memories": [card.model_dump(mode="json") for card in direct_cards],
            "k": options.similarity_k,
        }
        selection_result = await provider.complete_structured(
            _message(
                selection_payload,
                "Select only topically relevant memory IDs; return zero to k IDs.",
            ),
            schema={"type": "object"},
            model=options.model,
            temperature=options.temperature,
            max_output_tokens=120,
            seed=options.seed,
            timeout_seconds=options.timeout_seconds,
            metadata={"operation": "select"},
        )
        selected_ids = set(selection_result.parsed.get("selected_memory_ids", []))
        chosen = [card for card in direct_cards if card.memory_id in selected_ids]
        decisions, admitted = _raw_views(chosen)
        selected = decisions
        generator_payload = {
            "current_message": context.current_message,
            "recent_turns": [turn.model_dump(mode="json") for turn in context.recent_turns],
            "raw_selected_cards": [card.model_dump(mode="json") for card in chosen],
            "admitted_memories": [item.model_dump(mode="json") for item in admitted],
        }
    else:
        raise ValueError(f"unsupported method: {method}")

    serialized_generator = json.dumps(generator_payload, ensure_ascii=False, sort_keys=True)
    started = time.perf_counter()
    generated_result = await provider.complete_structured(
        _message(generator_payload, prompt_loader.load("reconsider_lite/v1/generator_system.md")),
        schema=GeneratorOutput.model_json_schema(),
        model=options.model,
        temperature=options.temperature,
        max_output_tokens=options.max_output_tokens,
        seed=options.seed,
        timeout_seconds=options.timeout_seconds,
        metadata={"operation": "generate"},
    )
    stage.generation_ms = (time.perf_counter() - started) * 1000
    generated = GeneratorOutput.model_validate(generated_result.parsed)
    admitted_ids = {item.memory_id for item in admitted}
    rejected_cards = [
        card for card in context.candidate_memories if card.memory_id not in admitted_ids
    ]
    started = time.perf_counter()
    issues = validate_response(
        generated,
        admitted,
        rejected_cards,
        max_explicit_callbacks=options.max_explicit_callbacks,
    )
    stage.validation_ms = (time.perf_counter() - started) * 1000
    repair_count = 0
    fallback_type = None
    if issues:
        repair_count = 1
        reduced = GeneratorContext(
            current_message=context.current_message,
            recent_turns=context.recent_turns,
            admitted_memories=admitted,
        )
        repaired = await repair_once(
            provider,
            reduced,
            generated,
            [issue.code for issue in issues],
            model=options.model,
            seed=options.seed,
        )
        second_issues = validate_response(
            repaired,
            admitted,
            rejected_cards,
            max_explicit_callbacks=options.max_explicit_callbacks,
        )
        if second_issues:
            generated, fallback_type = deterministic_fallback(context.current_message, admitted)
            issues = second_issues
        else:
            generated = repaired
            issues = []

    actions = {item.memory_id: item.action for item in decisions}
    for gate in gates.results:
        actions.setdefault(gate.memory_id, PublicAction.IGNORE)
    prompts_root = repo_root() / "prompts"
    hashes = hash_prompt_files(prompts_root)
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root(),
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        commit = None
    return RunRecord(
        run_id=f"run_{uuid.uuid4().hex[:16]}",
        campaign_id=options.campaign_id,
        scenario_id=scenario.scenario_id,
        scenario_version=scenario.version,
        method=method,
        provider=provider.name,
        model_id=options.model,
        prompt_versions={"reconsider_lite": "v1"},
        prompt_hashes=hashes,
        config_hash=_json_hash(options.__dict__),
        random_seed=options.seed,
        candidate_order=[card.memory_id for card in context.candidate_memories],
        hard_gates=gates,
        deliberation=deliberation,
        controller_decisions=decisions,
        admitted_views=admitted,
        visible_reply=generated.reply,
        actions=actions,
        validator_issues=issues,
        repair_count=repair_count,
        fallback_type=fallback_type,
        latency=stage,
        token_usage={
            "input": generated_result.input_tokens or 0,
            "output": generated_result.output_tokens or 0,
        },
        schema_valid=generated_result.schema_valid,
        input_hash=_json_hash(context.model_dump(mode="json")),
        output_hash=_json_hash(generated.model_dump(mode="json")),
        generator_request_json=serialized_generator,
        software_commit_hash=commit,
        extra=extra,
    )

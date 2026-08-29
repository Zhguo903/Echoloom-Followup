from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from bbi.domain.scenarios import Scenario
from bbi.scenarios.manifests import load_manifest, scenarios_from_manifest

HELDOUT_MINIMUMS = {
    "beneficial_use_retention": 16,
    "no_memory_best": 12,
    "stale_state_use": 10,
    "wrong_branch_use": 8,
    "cross_domain": 10,
    "sensitive_disclosure": 10,
    "callback_fatigue": 8,
    "episode_to_trait": 8,
    "required_qualifier": 12,
    "conflicting_memories": 8,
    "explicit_history_request": 12,
    "candidate_order_stress": 12,
    "human_disagreement_expected": 12,
}

SEPARATION_CATEGORIES = {
    "wrong_user",
    "wrong_branch",
    "deleted_do_not_use",
    "superseded_corrected",
    "sensitive_canary",
    "callback_fatigue",
    "episode_to_identity",
    "relevant_cross_domain",
}


def _review_summary(scenarios: list[Scenario]) -> dict[str, int]:
    return {
        "needs_human_review": sum(
            scenario.review.content_review_status == "needs_human_review"
            or scenario.review.research_review_status == "needs_human_review"
            for scenario in scenarios
        ),
        "fully_human_reviewed": sum(
            scenario.review.content_review_status == "human_reviewed"
            and scenario.review.research_review_status == "human_reviewed"
            for scenario in scenarios
        ),
    }


def _heldout_report(scenarios: list[Scenario]) -> dict[str, Any]:
    domain_counts = Counter(scenario.domain for scenario in scenarios)
    action_counts = Counter(
        scenario.focal_action_profile.value
        for scenario in scenarios
        if scenario.focal_action_profile is not None
    )
    domain_actions: dict[str, set[str]] = defaultdict(set)
    for scenario in scenarios:
        if scenario.focal_action_profile is not None:
            domain_actions[scenario.domain].add(scenario.focal_action_profile.value)
    tag_counts = Counter(tag for scenario in scenarios for tag in scenario.tags)
    violations: list[str] = []
    if len(scenarios) != 48:
        violations.append(f"expected 48 scenarios; found {len(scenarios)}")
    if len(domain_counts) != 12 or any(count != 4 for count in domain_counts.values()):
        violations.append("expected 12 domains with four scenarios each")
    expected_actions = {"ignore", "scoped_implicit", "scoped_explicit", "ask_first"}
    for domain, actions in sorted(domain_actions.items()):
        if actions != expected_actions:
            violations.append(f"{domain} does not contain all four focal profiles")
    if any(len(scenario.candidate_memories) != 6 for scenario in scenarios):
        violations.append("every held-out scenario must contain exactly six candidate cards")
    minimum_results = {}
    for tag, minimum in HELDOUT_MINIMUMS.items():
        observed = tag_counts[tag]
        minimum_results[tag] = {"minimum": minimum, "observed": observed, "pass": observed >= minimum}
        if observed < minimum:
            violations.append(f"{tag}: expected at least {minimum}; found {observed}")
    return {
        "corpus_kind": "heldout_core",
        "scenario_count": len(scenarios),
        "domain_counts": dict(sorted(domain_counts.items())),
        "focal_action_counts": dict(sorted(action_counts.items())),
        "cross_cutting_minimums": minimum_results,
        "candidate_count_distribution": dict(
            sorted(Counter(len(scenario.candidate_memories) for scenario in scenarios).items())
        ),
        "structural_status": "pass" if not violations else "fail",
        "violations": violations,
        "review": _review_summary(scenarios),
        "research_readiness": "not_evaluable",
    }


def _separation_report(scenarios: list[Scenario]) -> dict[str, Any]:
    categories = Counter(
        scenario.separation_stress.category
        for scenario in scenarios
        if scenario.separation_stress is not None
    )
    canaries: list[str] = []
    violations: list[str] = []
    if len(scenarios) != 16:
        violations.append(f"expected 16 scenarios; found {len(scenarios)}")
    if set(categories) != SEPARATION_CATEGORIES or any(count != 2 for count in categories.values()):
        violations.append("expected two scenarios in each of eight separation categories")
    for scenario in scenarios:
        metadata = scenario.separation_stress
        if metadata is None:
            violations.append(f"missing separation metadata: {scenario.scenario_id}")
            continue
        canaries.append(metadata.exact_canary)
        card = next(
            (
                item
                for item in scenario.candidate_memories
                if item.memory_id == metadata.rejected_memory_id
            ),
            None,
        )
        if card is None or card.content.count(metadata.exact_canary) != 1:
            violations.append(f"invalid exact canary placement: {scenario.scenario_id}")
        if metadata.exact_canary in str(scenario.to_participant_view(study="study_a")):
            violations.append(f"canary leaked to participant-safe view: {scenario.scenario_id}")
        if set(metadata.required_checks) != {
            "exact_canary",
            "lexical_overlap",
            "blinded_semantic",
        }:
            violations.append(f"incomplete check plan: {scenario.scenario_id}")
    if len(canaries) != len(set(canaries)):
        violations.append("separation canaries are not unique")
    return {
        "corpus_kind": "separation_stress",
        "scenario_count": len(scenarios),
        "category_counts": dict(sorted(categories.items())),
        "unique_canary_count": len(set(canaries)),
        "structural_status": "pass" if not violations else "fail",
        "violations": violations,
        "review": _review_summary(scenarios),
        "research_readiness": "not_evaluable",
    }


def coverage_report(root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    scenarios = scenarios_from_manifest(root, manifest)
    set_name = manifest.get("set_name")
    if set_name == "heldout_core_v1":
        report = _heldout_report(scenarios)
    elif set_name == "separation_stress_v1":
        report = _separation_report(scenarios)
    else:
        report = {
            "corpus_kind": set_name,
            "scenario_count": len(scenarios),
            "structural_status": "pass",
            "violations": [],
            "review": _review_summary(scenarios),
            "research_readiness": "not_evaluable",
        }
    report["manifest"] = str(manifest_path.relative_to(root))
    report["manifest_frozen"] = bool(manifest.get("frozen"))
    return report

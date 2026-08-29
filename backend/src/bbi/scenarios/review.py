import csv
from io import StringIO
from pathlib import Path

from bbi.domain.scenarios import Scenario
from bbi.scenarios.manifests import load_manifest, scenarios_from_manifest

QUEUE_FIELDS = [
    "scenario_id",
    "set_name",
    "domain",
    "focal_action_profile",
    "content_review_status",
    "research_review_status",
    "content_reviewer",
    "content_decision",
    "research_reviewer",
    "research_decision",
    "review_notes",
]


def review_markdown(scenarios: list[Scenario], manifest_path: Path) -> str:
    reviewed = sum(
        scenario.review.content_review_status == "human_reviewed"
        and scenario.review.research_review_status == "human_reviewed"
        for scenario in scenarios
    )
    lines = [
        "# Scenario Human-Review Report",
        "",
        f"Manifest: `{manifest_path}`",
        "",
        f"- Drafts in queue: {len(scenarios)}",
        f"- Fully human reviewed: {reviewed}",
        f"- Still needs human review: {len(scenarios) - reviewed}",
        "- Research readiness: `not_evaluable`",
        "- Corpus frozen: no",
        "",
        "Automated lint and coverage do not count as human content or research review. Blank queue fields are intentional.",
        "",
        "| scenario_id | domain | focal profile | content review | research review | reviewers |",
        "|---|---|---|---|---|---|",
    ]
    for scenario in scenarios:
        profile = scenario.focal_action_profile.value if scenario.focal_action_profile else "none"
        lines.append(
            f"| {scenario.scenario_id} | {scenario.domain} | {profile} | "
            f"{scenario.review.content_review_status} | "
            f"{scenario.review.research_review_status} | "
            f"{', '.join(scenario.review.reviewed_by)} |"
        )
    lines.extend(
        [
            "",
            "See `docs/SCENARIO_REVIEW_PROTOCOL.md` for the required 10 held-out checks and five additional separation checks.",
            "",
        ]
    )
    return "\n".join(lines)


def review_queue_csv(scenarios: list[Scenario]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=QUEUE_FIELDS, lineterminator="\n")
    writer.writeheader()
    for scenario in scenarios:
        writer.writerow(
            {
                "scenario_id": scenario.scenario_id,
                "set_name": scenario.set_name,
                "domain": scenario.domain,
                "focal_action_profile": scenario.focal_action_profile.value
                if scenario.focal_action_profile
                else "",
                "content_review_status": scenario.review.content_review_status,
                "research_review_status": scenario.review.research_review_status,
                "content_reviewer": "",
                "content_decision": "",
                "research_reviewer": "",
                "research_decision": "",
                "review_notes": "",
            }
        )
    return output.getvalue()


def build_review_outputs(
    root: Path,
    manifest_path: Path,
    report_path: Path,
    queue_path: Path,
) -> tuple[Path, Path]:
    manifest = load_manifest(manifest_path)
    scenarios = scenarios_from_manifest(root, manifest)
    displayed_manifest = (
        manifest_path.relative_to(root) if manifest_path.is_relative_to(root) else manifest_path
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(review_markdown(scenarios, displayed_manifest), encoding="utf-8")
    queue_path.write_text(review_queue_csv(scenarios), encoding="utf-8")
    return report_path, queue_path


def build_combined_review_queue(
    root: Path, manifest_paths: list[Path], queue_path: Path
) -> Path:
    scenarios = []
    for manifest_path in manifest_paths:
        scenarios.extend(scenarios_from_manifest(root, load_manifest(manifest_path)))
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.write_text(review_queue_csv(scenarios), encoding="utf-8")
    return queue_path

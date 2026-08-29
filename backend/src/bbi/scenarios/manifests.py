import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from bbi.evaluation.scenarios import load_scenario


def file_sha256(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _git_state(root: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


def build_corpus_manifest(
    root: Path,
    scenario_dir: Path,
    *,
    corpus_id: str,
) -> dict[str, Any]:
    files = sorted(scenario_dir.glob("*.yaml"))
    if not files:
        raise ValueError(f"no scenario files found: {scenario_dir}")
    scenarios = [load_scenario(path) for path in files]
    set_names = {scenario.set_name for scenario in scenarios}
    if len(set_names) != 1:
        raise ValueError(f"manifest requires one set_name; found {sorted(set_names)}")
    commit, dirty = _git_state(root)
    runbook_phase2 = root.parent / "runbook_phase2.md"
    authoring_sources = {}
    for relative in (
        Path("docs/HELDOUT_SCENARIO_MATRIX.md"),
        Path("docs/SCENARIO_REVIEW_PROTOCOL.md"),
        Path("docs/SEPARATION_EXPERIMENT.md"),
    ):
        source = root / relative
        if source.exists():
            authoring_sources[str(relative)] = file_sha256(source)
    entries = []
    for path, scenario in zip(files, scenarios, strict=True):
        entries.append(
            {
                "scenario_id": scenario.scenario_id,
                "version": scenario.version,
                "path": str(path.relative_to(root)),
                "domain": scenario.domain,
                "focal_action_profile": scenario.focal_action_profile,
                "scenario_hash": scenario.participant_visible_hash(),
                "file_hash": file_sha256(path),
                "status": scenario.status,
                "content_review_status": scenario.review.content_review_status,
                "research_review_status": scenario.review.research_review_status,
                "reviewed_by": scenario.review.reviewed_by,
            }
        )
    return {
        "manifest_version": 1,
        "corpus_id": corpus_id,
        "set_name": set_names.pop(),
        "status": "draft",
        "frozen": False,
        "generated_at": datetime.now(UTC).isoformat(),
        "repository_commit": commit,
        "repository_dirty": dirty,
        "runbook_hashes": {
            "runbook.md": file_sha256(root / "runbook.md"),
            "runbook_phase2.md": file_sha256(runbook_phase2)
            if runbook_phase2.exists()
            else None,
        },
        "authoring_source_hashes": authoring_sources,
        "scenario_count": len(entries),
        "entries": entries,
        "research_note": (
            "Unreviewed synthetic drafts. This manifest is not a research freeze and is not "
            "eligible for participant collection or a real-model campaign."
        ),
    }


def write_manifest(manifest: dict[str, Any], destination: Path) -> Path:
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite manifest: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return destination


def load_manifest(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("entries"), list):
        raise ValueError(f"invalid corpus manifest: {path}")
    return value


def scenarios_from_manifest(root: Path, manifest: dict[str, Any]):  # type: ignore[no-untyped-def]
    return [load_scenario(root / entry["path"]) for entry in manifest["entries"]]


def freeze_corpus(root: Path, manifest_path: Path) -> Path:
    """Create a separate freeze record only when every scenario has human approval."""

    manifest = load_manifest(manifest_path)
    scenarios = scenarios_from_manifest(root, manifest)
    blockers = [
        scenario.scenario_id
        for scenario in scenarios
        if scenario.status not in {"reviewed", "frozen"}
        or scenario.review.content_review_status != "human_reviewed"
        or scenario.review.research_review_status != "human_reviewed"
        or not scenario.review.reviewed_by
    ]
    if blockers:
        raise ValueError(
            "refusing to freeze unreviewed scenarios: " + ", ".join(blockers[:8])
        )
    destination = manifest_path.with_name(f"{manifest_path.stem}.frozen.json")
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite freeze: {destination}")
    frozen = {
        **manifest,
        "status": "frozen",
        "frozen": True,
        "frozen_at": datetime.now(UTC).isoformat(),
        "source_manifest_hash": file_sha256(manifest_path),
    }
    destination.write_text(
        json.dumps(frozen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return destination

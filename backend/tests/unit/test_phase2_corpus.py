import csv

import pytest
from bbi.evaluation.scenarios import discover_scenarios, lint_scenarios
from bbi.scenarios.coverage import coverage_report
from bbi.scenarios.manifests import (
    build_corpus_manifest,
    freeze_corpus,
    load_manifest,
    write_manifest,
)
from bbi.scenarios.review import build_combined_review_queue, build_review_outputs
from bbi.scenarios.scaffold import scaffold_heldout, scaffold_separation


def test_phase2_corpus_counts_and_review_states(root):  # type: ignore[no-untyped-def]
    scenarios = discover_scenarios([root / "data/scenarios"])
    assert len(scenarios) == 88
    assert sum(scenario.set_name == "dev_v1" for scenario in scenarios) == 24
    assert sum(scenario.set_name == "heldout_core_v1" for scenario in scenarios) == 48
    assert sum(scenario.set_name == "separation_stress_v1" for scenario in scenarios) == 16
    drafts = [scenario for scenario in scenarios if scenario.set_name != "dev_v1"]
    assert all(scenario.status == "draft" for scenario in drafts)
    assert all(scenario.review.content_review_status == "needs_human_review" for scenario in drafts)
    assert all(scenario.review.research_review_status == "needs_human_review" for scenario in drafts)
    assert all(scenario.review.reviewed_by == [] for scenario in drafts)


def test_phase2_manifests_and_structural_coverage_pass(root):  # type: ignore[no-untyped-def]
    heldout_path = root / "data/manifests/heldout_core_v1.json"
    separation_path = root / "data/manifests/separation_stress_v1.json"
    heldout_manifest = load_manifest(heldout_path)
    separation_manifest = load_manifest(separation_path)
    assert heldout_manifest["scenario_count"] == 48
    assert separation_manifest["scenario_count"] == 16
    assert heldout_manifest["frozen"] is False
    assert separation_manifest["frozen"] is False
    heldout = coverage_report(root, heldout_path)
    separation = coverage_report(root, separation_path)
    assert heldout["structural_status"] == "pass"
    assert heldout["focal_action_counts"] == {
        "ask_first": 12,
        "ignore": 12,
        "scoped_explicit": 12,
        "scoped_implicit": 12,
    }
    assert set(heldout["domain_counts"].values()) == {4}
    assert all(value["pass"] for value in heldout["cross_cutting_minimums"].values())
    assert separation["structural_status"] == "pass"
    assert set(separation["category_counts"].values()) == {2}
    assert separation["unique_canary_count"] == 16


def test_all_phase2_scenarios_lint_and_safe_views_hide_canaries(root):  # type: ignore[no-untyped-def]
    assert lint_scenarios([root / "data/scenarios"]) == []
    scenarios = discover_scenarios([root / "data/scenarios/separation_stress_v1"])
    canaries = []
    for scenario in scenarios:
        assert scenario.separation_stress is not None
        canary = scenario.separation_stress.exact_canary
        canaries.append(canary)
        assert canary not in str(scenario.to_participant_view(study="study_a"))
        assert "author_expectations" not in scenario.to_model_input_view()
    assert len(canaries) == len(set(canaries)) == 16


def test_freeze_refuses_unreviewed_drafts(root):  # type: ignore[no-untyped-def]
    manifest = root / "data/manifests/heldout_core_v1.json"
    with pytest.raises(ValueError, match="refusing to freeze unreviewed"):
        freeze_corpus(root, manifest)
    assert not manifest.with_name("heldout_core_v1.frozen.json").exists()


def test_combined_human_review_queue_has_blank_human_decisions(root):  # type: ignore[no-untyped-def]
    queue = root / "reports/phase2/human_review_queue.csv"
    with queue.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 64
    assert all(row["content_reviewer"] == "" for row in rows)
    assert all(row["content_decision"] == "" for row in rows)
    assert all(row["research_reviewer"] == "" for row in rows)
    assert all(row["research_decision"] == "" for row in rows)


def test_scaffold_manifest_and_review_tools_are_reproducible(root, tmp_path):  # type: ignore[no-untyped-def]
    heldout_dir = tmp_path / "heldout"
    separation_dir = tmp_path / "separation"
    heldout_paths = scaffold_heldout(root / "docs/HELDOUT_SCENARIO_MATRIX.md", heldout_dir)
    separation_paths = scaffold_separation(separation_dir)
    assert len(heldout_paths) == 48
    assert len(separation_paths) == 16
    assert lint_scenarios([heldout_dir, separation_dir]) == []
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        scaffold_heldout(root / "docs/HELDOUT_SCENARIO_MATRIX.md", heldout_dir)

    manifest = build_corpus_manifest(
        root,
        root / "data/scenarios/heldout_core_v1",
        corpus_id="heldout_core_v1_test",
    )
    assert manifest["scenario_count"] == 48
    assert manifest["frozen"] is False
    manifest_path = write_manifest(manifest, tmp_path / "manifest.json")
    with pytest.raises(FileExistsError, match="refusing to overwrite manifest"):
        write_manifest(manifest, manifest_path)
    report_path, queue_path = build_review_outputs(
        root,
        root / "data/manifests/heldout_core_v1.json",
        tmp_path / "review.md",
        tmp_path / "review.csv",
    )
    assert "Fully human reviewed: 0" in report_path.read_text(encoding="utf-8")
    assert len(queue_path.read_text(encoding="utf-8").splitlines()) == 49
    combined = build_combined_review_queue(
        root,
        [
            root / "data/manifests/heldout_core_v1.json",
            root / "data/manifests/separation_stress_v1.json",
        ],
        tmp_path / "combined.csv",
    )
    assert len(combined.read_text(encoding="utf-8").splitlines()) == 65

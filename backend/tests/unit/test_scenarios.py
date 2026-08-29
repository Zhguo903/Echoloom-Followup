from bbi.evaluation.scenarios import coverage_matrix, discover_scenarios, lint_scenarios


def test_synthetic_corpus_lints_and_covers_required_size(root):  # type: ignore[no-untyped-def]
    path = root / "data/scenarios"
    assert lint_scenarios([path]) == []
    scenarios = discover_scenarios([path])
    assert len(scenarios) >= 24
    assert sum("development_golden" in item.tags for item in scenarios) == 10
    coverage = coverage_matrix(scenarios)
    assert "sensitive_history" in coverage["memory_types"]
    assert "wrong_branch_use" in coverage["failure_modes"]

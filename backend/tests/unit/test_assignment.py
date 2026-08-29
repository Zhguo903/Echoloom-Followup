from collections import Counter

from bbi.study.assignment import generate_incomplete_block


def test_assignment_is_reproducible_balanced_and_nonduplicating():
    args = (["s1", "s2"], ["a", "b", "c", "d"])
    first = generate_incomplete_block(*args, participants=24, seed=8)
    second = generate_incomplete_block(*args, participants=24, seed=8)
    assert first == second
    assert all(len(set(item.blinded_conditions)) == 2 for item in first)
    counts = Counter(
        (item.scenario_id, condition) for item in first for condition in item.blinded_conditions
    )
    assert max(counts.values()) - min(counts.values()) <= 1

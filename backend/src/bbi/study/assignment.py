import random
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Assignment:
    participant_index: int
    scenario_id: str
    blinded_conditions: tuple[str, ...]
    display_order: tuple[str, ...]
    seed: int


def generate_incomplete_block(
    scenario_ids: list[str],
    conditions: list[str],
    *,
    participants: int,
    conditions_per_scenario: int = 2,
    seed: int = 454491,
) -> list[Assignment]:
    if conditions_per_scenario > len(conditions):
        raise ValueError("block cannot contain more conditions than exist")
    rng = random.Random(seed)
    exposure: Counter[tuple[str, str]] = Counter()
    assignments: list[Assignment] = []
    for participant in range(participants):
        scenario = scenario_ids[participant % len(scenario_ids)]
        ranked = sorted(
            conditions, key=lambda condition: (exposure[(scenario, condition)], rng.random())
        )
        chosen = tuple(ranked[:conditions_per_scenario])
        display = list(chosen)
        rng.shuffle(display)
        for condition in chosen:
            exposure[(scenario, condition)] += 1
        assignments.append(Assignment(participant, scenario, chosen, tuple(display), seed))
    return assignments

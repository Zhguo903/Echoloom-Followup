from collections.abc import Callable

import numpy as np


def clustered_bootstrap(
    values_by_cluster: dict[str, list[float]],
    statistic: Callable[[list[float]], float] | None = None,
    *,
    replicates: int = 2_000,
    seed: int = 454491,
) -> tuple[float, float, float]:
    statistic = statistic or (lambda values: float(np.mean(values)) if values else float("nan"))
    clusters = sorted(values_by_cluster)
    observed_values = [value for cluster in clusters for value in values_by_cluster[cluster]]
    observed = statistic(observed_values)
    if not clusters:
        return observed, float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    estimates = []
    for _ in range(replicates):
        sampled = rng.choice(clusters, size=len(clusters), replace=True)
        values = [value for cluster in sampled for value in values_by_cluster[str(cluster)]]
        estimates.append(statistic(values))
    low, high = np.nanpercentile(estimates, [2.5, 97.5])
    return observed, float(low), float(high)

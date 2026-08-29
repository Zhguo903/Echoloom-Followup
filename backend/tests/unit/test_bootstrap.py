from bbi.evaluation.bootstrap import clustered_bootstrap


def test_bootstrap_is_deterministic():
    values = {"a": [0.0, 1.0], "b": [1.0, 1.0]}
    assert clustered_bootstrap(values, replicates=100, seed=7) == clustered_bootstrap(
        values, replicates=100, seed=7
    )

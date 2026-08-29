# Evaluation

The synthetic corpus is separated by purpose:

- `dev_v1`: 24 development examples (the former 10 golden + 14 core fixtures), migrated without changing their conversation or memory content;
- `heldout_core_v1`: 48 coding-agent drafts covering 12 domains × four focal action profiles;
- `separation_stress_v1`: 16 coding-agent drafts covering eight rejected-context categories × two variants.

All expected actions are stored as `author_expectations` with status `provisional_design_hypothesis`. They allow sets of actions and are never treated as universal preferences or sent to models. The 64 new drafts have zero human reviews and are not frozen.

The harness reports action match, unsafe action, action distribution, adaptive empty set, controller overrides, beneficial-use retention, leakage, repair/fallback, schema validity, and latency. Reports split by scenario, family, memory type, failure mode, and method. Clustered bootstrap resamples scenario families with 2,000 fixed-seed replicates.

The optional blinded LLM judge is secondary and never replaces deterministic checks or later human distributions. A different model family should be used where feasible, with identity and disagreement recorded.

Structural coverage reports live under `reports/phase2/`. A `pass` there means only that counts, domains, profiles, tags, candidate-card structure, and canary uniqueness meet the drafting specification. Research readiness is `not_evaluable` until human review and later authorized phases are complete.

## Go/no-go interpretation

- Baseline headroom: if simple baselines solve nearly all cases, narrow the contribution or improve non-trivial scenarios.
- Beneficial-use guardrail: report relative retention; do not call blanket suppression a success.
- Context separation: if no empirical signal appears, describe it as an engineering safeguard.
- Study headroom is `not_evaluable` without approved pilot data.

Useful null outcomes include no universal action, ask-first friction, two-pass gains without rubric gains, provider variability, no separation effect, selection changes without experience changes, baseline dominance, and over-suppression. Each limits claims and motivates a discriminating next study rather than a positive rewrite.

# Evaluation

The synthetic corpus has 10 golden cases and 14 core variants. Gold labels allow sets of acceptable actions; they are stimulus/evaluation scaffolding, not universal preferences.

The harness reports action match, unsafe action, action distribution, adaptive empty set, controller overrides, beneficial-use retention, leakage, repair/fallback, schema validity, and latency. Reports split by scenario, family, memory type, failure mode, and method. Clustered bootstrap resamples scenario families with 2,000 fixed-seed replicates.

The optional blinded LLM judge is secondary and never replaces deterministic/gold checks. A different model family should be used where feasible, with identity and disagreement recorded.

## Go/no-go interpretation

- Baseline headroom: if simple baselines solve nearly all cases, narrow the contribution or improve non-trivial scenarios.
- Beneficial-use guardrail: report relative retention; do not call blanket suppression a success.
- Context separation: if no empirical signal appears, describe it as an engineering safeguard.
- Study headroom is `not_evaluable` without approved pilot data.

Useful null outcomes include no universal action, ask-first friction, two-pass gains without rubric gains, provider variability, no separation effect, selection changes without experience changes, baseline dominance, and over-suppression. Each limits claims and motivates a discriminating next study rather than a positive rewrite.


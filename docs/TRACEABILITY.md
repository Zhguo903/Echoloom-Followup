# Design Traceability

| Requirement | Operational question | Mechanism | Signals | Code/tests |
|---|---|---|---|---|
| DR1 Relational utility | Would use materially help? | Utility judgment, adaptive `k = 0`, and held-out retain/no-memory profiles | retention, low-value use, helpfulness | `backend/src/bbi/pipeline/controller.py`, `heldout_core_v1` tags, `test_controller.py` |
| DR2 Conversational warrant | Is there a present reason? | Warrant gate; sensitivity raises threshold; neutral ask-first drafts | unwarranted callbacks, intrusion | `backend/src/bbi/pipeline/controller.py`, `docs/HELDOUT_SCENARIO_MATRIX.md` |
| DR3 Scope preservation | What exact meaning and qualifiers survive? | currentness/branch gates, admitted views, validators, qualifier coverage | stale/wrong-branch use, qualifier fidelity | `backend/src/bbi/gates/`, `backend/src/bbi/validation/`, `reports/phase2/heldout_coverage.json` |
| DR4 Controlled visibility | Should use be silent, implicit, explicit, or permissioned? | expression action, sanitized topic, explicit cap, separation canaries | action distribution, privacy, agency, rejected-context influence | `backend/src/bbi/pipeline/context_builder.py`, `separation_stress_v1`, P0 tests |

Traceability is procedural scaffolding, not evidence that any action is universally preferred.

Scenario-v2 safe views and prompt audits are implemented in `backend/src/bbi/domain/scenarios.py` and `backend/src/bbi/validation/label_leakage.py`. Migration and leakage tests live in `backend/tests/unit/test_scenario_v2.py`; corpus count, coverage, canary, review-state, and freeze-refusal tests live in `backend/tests/unit/test_phase2_corpus.py`.

The 48 held-out and 16 separation items remain authoring drafts. Passing structural coverage links requirements to planned stressors; it does not establish a metric result or human preference.

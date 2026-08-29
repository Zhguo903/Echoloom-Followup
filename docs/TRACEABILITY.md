# Design Traceability

| Requirement | Operational question | Mechanism | Signals | Code/tests |
|---|---|---|---|---|
| DR1 Relational utility | Would use materially help? | Utility judgment and adaptive `k = 0` | retention, low-value use, helpfulness | `pipeline/controller.py`, `test_controller.py` |
| DR2 Conversational warrant | Is there a present reason? | Warrant gate; sensitivity raises threshold | unwarranted callbacks, intrusion | `pipeline/controller.py`, scenario tags |
| DR3 Scope preservation | What exact meaning and qualifiers survive? | currentness/branch gates, admitted views, validators | stale/wrong-branch use, qualifier fidelity | `gates/`, `validation/` |
| DR4 Controlled visibility | Should use be silent, implicit, explicit, or permissioned? | expression action, sanitized topic, explicit cap | action distribution, privacy, agency | `pipeline/context_builder.py`, P0 tests |

Traceability is procedural scaffolding, not evidence that any action is universally preferred.


# Scenario Authoring

1. Start with a mild, non-clinical current need and a small candidate set.
2. Use only invented names/content and explicitly synthetic provenance such as `synthetic_authoring`.
3. Preserve owner, character, branch, correction, confidence, sensitivity, permission, callback count, and required qualifiers.
4. Give every card a non-empty provisional `acceptable_actions_by_memory` set; allow multiple actions where judgment is plausibly contested.
5. Add harmful/beneficial opportunities and unique canaries for leakage pressure.
6. Include negative cases and avoid obvious lexical labels that make the policy trivial.
7. Mark expectations `provisional_design_hypothesis`; never call author expectations human truth or participant preference.
8. Set coding-agent drafts to `status: draft`, both review states to `needs_human_review`, and `reviewed_by: []`.
9. Increment scenario version when participant-visible context, cards, provisional action sets, or expected failure tags change.
10. Never edit a reviewed/frozen item in place; create a new version and reset affected review states.

Run `uv run bbi scenario-lint data/scenarios`. It validates models, IDs, references, branch consistency, sanitized topics, canary uniqueness, obvious PII patterns, and forbidden real-interview source labels.

Use `docs/SCENARIO_REVIEW_PROTOCOL.md` for human review. Automated lint and matrix coverage never populate reviewer fields. `corpus-freeze` intentionally refuses every current Phase 2 manifest.

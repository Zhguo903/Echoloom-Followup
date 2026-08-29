# Scenario Authoring

1. Start with a mild, non-clinical current need and a small candidate set.
2. Use only invented names/content and `synthetic_user_message` provenance.
3. Preserve owner, character, branch, correction, confidence, sensitivity, permission, callback count, and required qualifiers.
4. Give every card a non-empty acceptable-action set; allow multiple actions where judgment is plausibly contested.
5. Add harmful/beneficial opportunities and unique canaries for leakage pressure.
6. Include negative cases and avoid obvious lexical labels that make the policy trivial.
7. Mark claim status `design_hypothesis`; never call gold “participant preference.”
8. Increment scenario version when the context, cards, gold sets, or expected failure tags change.

Run `uv run bbi scenario-lint data/scenarios`. It validates models, IDs, references, branch consistency, sanitized topics, canary uniqueness, obvious PII patterns, and forbidden real-interview source labels.


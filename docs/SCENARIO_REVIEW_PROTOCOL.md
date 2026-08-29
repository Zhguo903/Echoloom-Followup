# Scenario Review Protocol

All Phase 2 scenarios are synthetic coding-agent drafts. Automated checks may catch schema, coverage, PII-pattern, and reference errors, but only a human reviewer may change either review state to `human_reviewed`, populate `reviewed_by`, approve research use, or freeze a corpus.

## Required independent decisions

Record content review and research review separately. A reviewer must inspect the rendered participant-safe view as well as the researcher view.

For every held-out draft, check:

1. The current message sounds natural and gives a concrete present need.
2. The fictional situation is understandable without internal research terminology.
3. Wording does not lead the reviewer toward one of the four action options.
4. At least three candidate memories are superficially tempting to a relevance-only method.
5. The focal action hypothesis is not disclosed in participant-visible text.
6. The content is mild, non-clinical, synthetic, and free of real private material or obvious PII.
7. Required time, source, uncertainty, branch, or episode qualifiers are explicit.
8. The item is substantively distinct from the 24 development scenarios.
9. Any future Study A target set can be judged independently; this draft does not preselect it.
10. Any future Study B context would be sufficient without exposing method/provider/model labels.

For every separation-stress draft, additionally check:

11. The designated rejected card contains exactly one unique canary string.
12. The canary has a natural semantic concept that a blinded reviewer could look for without seeing the canary.
13. The present request is fully answerable through the admitted card or a no-memory response.
14. Exact-canary, lexical-overlap, and optional blinded-semantic checks are predeclared.
15. The stress manipulation is compatible with shared hard gates; if not, record the boundary for Phase 7 instead of silently changing gate behavior.

## Review-state rules

- Coding-agent output: `status: draft`; both review states `needs_human_review`; `reviewed_by: []`.
- Content approval requires a named human reviewer and notes for any edits.
- Research approval requires a named human reviewer who checks non-triviality, separation validity, and claim boundaries.
- A text change after approval increments the scenario version and resets the affected review state.
- `corpus-freeze` must refuse any manifest containing a draft or missing either human review.

The generated queue at `reports/phase2/human_review_queue.csv` intentionally leaves human decision columns blank.

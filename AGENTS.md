# Repository Guidance

- Read `runbook.md`, `docs/CLAIM_BOUNDARIES.md`, and `docs/TRACEABILITY.md` before changing core behavior.
- Never invent study findings, quotes, participant data, or effect sizes.
- Keep raw interviews and customer-discovery responses out of the repository.
- Apply the same hard gates and candidate pool across comparison methods.
- Preserve physical generator-context separation in the full method.
- Do not request or store chain-of-thought; store only brief audit rationales.
- Keep mock/offline mode fully functional and never expose API keys in frontend code.
- Version and hash prompts; do not edit a frozen campaign in place.
- Run `make lint`, `make typecheck`, `make test`, and affected end-to-end tests.
- Update documentation when schemas, prompts, methods, study fields, or visible behavior change.
- Do not add learned retrieval, a vector database, training, production companion scope, or manipulative retention without explicit approval.

# Phase-2 Research Validation Rules

- The existing 24 scenario labels are provisional author expectations, not human gold.
- Never include author expectations or future Study A human distributions in model prompts.
- Never include author expectations in Study A participant payloads.
- Never include method, model, provider, or validator labels in Study B participant payloads.
- Keep Study A and Study B collection disabled by default; do not reinterpret the legacy study lock as approval.
- Do not create fake participant records outside explicitly test-only fixtures.
- A coding agent may draft scenarios but may not mark them human reviewed or research frozen.
- Freeze scenario, prompt, protocol, and campaign versions before approved collection or real-model evaluation.
- Preserve human disagreement and null results; do not overwrite completed campaign or study directories.
- Run label-leakage, migration, coverage, review-state, physical-separation, and affected e2e tests.

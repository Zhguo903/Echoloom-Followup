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


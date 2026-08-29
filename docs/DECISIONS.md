# Implementation Decisions

## 2026-08-28 — Source resolution

- The available supervision proposal is `../Before_Bringing_It_Up_Supervision_Proposal_V4.pdf`; the runbook's parenthesized filename variant is absent.
- `Study_A_Focused_Qualitative_Analysis_Internal(1)(1).pdf` was not found. No claim or excerpt is inferred from it.
- The legacy prototype remains read-only at `../../CSC454/EchoLoom_Interactive_Demo_v1.0.zip`. The new repository has no runtime dependency on it.
- No interview, survey, slide screenshot, personal image, or private chat is copied.

## 2026-08-28 — Implementation scope

- The deterministic mock is the normative development and CI provider.
- Scenario files are synthetic authored fixtures. Gold labels are evaluation scaffolding, not participant findings.
- The frontend uses the permitted color direction but introduces its own code and visual composition.

## 2026-08-29 — Reproducibility and local constraints

- Campaign directories become immutable once `manifest.json` exists; the Make target reports an existing completed mock campaign rather than overwriting it.
- SQLite study responses are implemented but study routes remain HTTP 403 unless `BBI_STUDY_MODE=true`.
- Docker configuration is provided and built by CI, but the local host has no Docker executable, so no local image claim is made.
- Anthropic and Gemini remain guarded optional runtime modes; mock and the server-side OpenAI-compatible adapter are implemented and tested in the repository scope.

## 2026-08-29 — Phase 2 baseline preservation

- The working prototype is preserved at tag `prototype-v1-before-study-instrumentation` on commit `922f4ab`.
- Phase 2 work uses branch `codex/research-validation-v2`; the `codex/` prefix follows the local workspace convention.
- Because the baseline `export-runs` command cannot export all SQLite rows, the pre-Phase-2 backup uses SQLite's online backup command plus an ordered JSONL export. Both contain only existing local synthetic run data; no participant records exist.
- Only Phases 0–2 of `runbook_phase2.md` are authorized. Separate study infrastructure, campaign configs, real-provider runs, and research freeze decisions remain deferred.

## 2026-08-29 — Safe scenario-v2 migration

- Schema v2 stores candidate cards once at scenario top level and constructs `ConversationInput` only at the pipeline boundary. This avoids duplicating full cards in serialized scenarios while preserving the existing gate/controller interfaces.
- V1 documents are converted in memory to `author_expectations`; v2 serialization never writes the key `gold`. The old 24 byte-identical v1 files are retained under `legacy/scenarios_v1/`, while canonical v2 copies live under `data/scenarios/dev_v1/`.
- Every migrated development scenario remains `draft` with both review states `needs_human_review`; the migration does not infer a reviewer.
- Researcher, Study A/Study B participant, and model-input views are explicit. Model request construction applies a defensive forbidden-label-key audit before any provider call.

## 2026-08-29 — Draft corpus and freeze boundary

- Held-out scaffolding uses the versioned 12-domain × four-action matrix in `docs/HELDOUT_SCENARIO_MATRIX.md`; each item has six candidate-card roles and neutral participant wording.
- Study A/B eligibility remains false and no target items are selected. Metadata exists only so later authorized phases can version the decision explicitly.
- Separation scaffolding covers eight categories twice and predeclares exact, lexical, and blinded-semantic checks, but no paired campaign runner or effect claim is implemented in Phase 2.
- Draft manifests intentionally record the current baseline commit with `repository_dirty: true`, `status: draft`, and `frozen: false`. This is honest provenance for generated work-in-progress, not a final experiment freeze.
- `corpus-freeze` fails closed until every scenario is marked reviewed by named humans. The coding agent leaves all 64 reviewer decisions blank.

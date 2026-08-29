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


# Phase 2 Baseline Audit

Audit date: 2026-08-29 (America/Toronto)
Repository: `/Users/zihan/UofT/chi/before-bringing-it-up`

## Preservation point

- Baseline branch: `main`
- Baseline commit: `922f4abf0c8aa8d8adee5082cc1bea74301fab42`
- Baseline working tree: clean
- Protection tag: `prototype-v1-before-study-instrumentation`
- Phase 2 working branch: `codex/research-validation-v2`
- Original runbook SHA-256: `ab63fbb734832b9cce06587493ac0eb2aadf63cf279a720962e46bf462d09cba`
- Phase 2 runbook SHA-256: `1fe8e232e8335010dbade542b5a513411c1c6c1145c6055ae8724900b7217d67`

The existing repository was not rebuilt. The tag preserves the complete working prototype before any scenario-schema or corpus changes.

## Local synthetic-data backup

Before schema work, the local SQLite database contained 63 synthetic run rows and 0 study sessions. Two ignored local backups were created:

- `var/backups/pre_phase2_bbi.sqlite3` — SQLite online backup; integrity check `ok`; 63 run rows and 0 study sessions.
- `var/backups/pre_phase2_runs.jsonl` — 63 run rows; SHA-256 `c81d98a51c067aa0713b74c8469aa00687f6a9d1e1bc0f0cfdff1ede137aae80`.

The Phase 2 runbook's proposed `bbi export-runs --all --output ...` syntax is not available in the baseline CLI. The baseline command only exports a campaign directory. The audit therefore used SQLite's online backup API plus an equivalent ordered JSONL export. No database migration is needed in Phases 0–2, and the existing Alembic head remains `0001`.

## Existing scenario corpus

The baseline corpus contains exactly 24 synthetic schema-v1 scenarios. All have scenario version 1 and use provisional `gold` evaluation scaffolding.

Golden development subset (10):

- `golden_alternate_universe_v1`
- `golden_corrected_diet_v1`
- `golden_episode_not_identity_v1`
- `golden_no_memory_v1`
- `golden_record_store_weekend_v1`
- `golden_repeated_milestone_v1`
- `golden_sensitive_invited_v1`
- `golden_sensitive_uninvited_v1`
- `golden_shared_success_v1`
- `golden_unconfirmed_inference_v1`

Core development subset (14):

- `core_candidate_order_v1`
- `core_character_mismatch_v1`
- `core_conflicting_memories_v1`
- `core_deleted_memory_v1`
- `core_explicit_success_v1`
- `core_forbidden_memory_v1`
- `core_medium_sensitivity_weak_warrant_v1`
- `core_milestone_invited_v1`
- `core_owner_mismatch_v1`
- `core_permission_awkward_v1`
- `core_personal_fact_low_value_v1`
- `core_shared_joke_repetition_v1`
- `core_stable_preference_gift_v1`
- `core_uncertain_preference_v1`

Baseline lint passes. It covers 11 memory types and 20 failure-mode tags, including sensitive history, stale state, wrong owner/character/branch, callback fatigue, candidate-order stress, no-memory-best, beneficial-use retention, and `ASK_FIRST` friction.

## Methods, prompts, and runtime

- Implemented methods: `no_memory`, `similarity_top_k`, `one_pass_selective`, `relevance_two_pass`, `reconsider_lite`, and `no_physical_separation`.
- Prompt directories are version `v1` for Reconsider-Lite, baselines, and judges.
- Default provider/model: deterministic local `mock` / `mock-v1`.
- Python: 3.13.12; Node: 24.14.0.
- `uv.lock` SHA-256: `58b87acc454f340aee109eaab656241d6a965af53194cde9c9c231183e9487d3`.
- `pnpm-lock.yaml` SHA-256: `671563bf07302ada2a490f809a56737367875da035fd3fa2b6ff12e06eef4585`.

## Collection locks and storage

- The existing blinded response-study route is locked by default through `BBI_STUDY_MODE=false`.
- There is no Study A collection route or Study A participant schema.
- There is no separate `BBI_STUDY_A_MODE` or `BBI_STUDY_B_MODE` yet; those belong to later Phase 3/8 work and are intentionally not introduced or enabled here.
- No participant records were created during this audit.

## Baseline quality results

Commands run before repository modifications:

```text
make lint       PASS
make typecheck  PASS
make test       PASS
make e2e        PASS
make build      PASS
```

Detailed results:

- Ruff, ESLint, and Prettier: pass.
- mypy (64 source files) and TypeScript strict check: pass.
- Backend: 26 tests passed; total measured coverage 90.87%.
- Frontend: 3 tests passed.
- Playwright: 2 flows passed (desktop Chromium and 393 px mobile).
- Python sdist/wheel and production Vite build: pass.
- Existing deprecation warning: FastAPI's current `starlette.testclient` compatibility layer warns about future `httpx2` migration; it is not a test failure.

The successful Playwright flows exercise the running API/web app, record-store scenario, comparison/export, sandbox, and the default study lock. This is the Phase 0 app-runs check.

## Baseline gaps relevant to Phases 1–2

- Scenario files use `schema_version: 1`, nested candidate memories, `set`, and `gold` terminology.
- No explicit researcher, participant-safe, or model-safe scenario serializers exist.
- The scenario API returns the complete researcher object.
- No v2 migration command, corpus manifests, review queue, review-status model, or freeze guard exists.
- No independent held-out corpus exists; all 24 scenarios are development fixtures.
- No 12-domain/4-action coverage checker exists.
- No separation-stress draft set or canary coverage report exists.
- No human review has been recorded for any Phase 2 draft.
- No real-provider validation campaign or participant study has been run; this audit contains no efficacy findings.

These gaps define the authorized Phase 1–2 work. Study A/B collection, participant data, paid-provider campaigns, and research-validation claims remain out of scope.

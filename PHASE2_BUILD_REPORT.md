# Phase 2 Interim Build Report

Status date: 2026-08-29 (America/Toronto)
Authorized scope completed: `runbook_phase2.md` Phases 0, 1, and 2 only

## Repository and preservation

- Repository: `/Users/zihan/UofT/chi/before-bringing-it-up`
- Working branch: `codex/research-validation-v2`
- Preserved baseline commit: `922f4abf0c8aa8d8adee5082cc1bea74301fab42`
- Baseline tag: `prototype-v1-before-study-instrumentation`
- Final Phase 0–2 commit: the commit containing this report on branch `codex/research-validation-v2`; use `git log -1` for its immutable hash.
- Baseline audit: `docs/PHASE2_BASELINE_AUDIT.md`
- Local pre-change backups: `var/backups/pre_phase2_bbi.sqlite3` and `var/backups/pre_phase2_runs.jsonl` (ignored, synthetic local data only).

The repository was extended in place, not rebuilt. The 24 original v1 files are byte-preserved under `legacy/scenarios_v1/`; their canonical v2 counterparts are under `data/scenarios/dev_v1/`.

## What was implemented

### Phase 0 — audit and preserve

- Recorded commit, clean state, scenario IDs/counts, methods, prompt versions, locks, Alembic head, dependency hashes, baseline gaps, and exact test results.
- Tagged the working prototype and created a dedicated branch.
- Backed up 63 existing synthetic run rows; the database contained zero study sessions.
- Recorded the baseline CLI deviation: it lacks the Phase 2 runbook's proposed `export-runs --all --output` flags, so an online SQLite backup and ordered JSONL export were used instead.

### Phase 1 — schema and terminology

- Added canonical Scenario v2 with top-level candidate cards, `set_name`, domain/action profile, study eligibility metadata, explicit review state, and optional separation metadata.
- Replaced runtime/evaluation `gold` terminology with `author_expectations` and mandatory `provisional_design_hypothesis` status.
- Kept v1 loading through an in-memory migration; v2 serialization rejects and never emits `gold`.
- Added `to_researcher_view()`, Study A/B `to_participant_view()`, and `to_model_input_view()`.
- Added participant-visible hashing and a defensive provider-request audit for author/human label keys.
- Updated the pipeline, metrics, API/frontend types, exported JSON Schema/OpenAPI, configs, and tests to use v2 safely.
- Retired the old v1 generator with a fail-safe notice so it cannot recreate or overwrite the original corpus.

No Alembic/database schema migration was needed or applied; the database remains at migration head `0001`.

### Phase 2 — corpus and review tooling

- Added held-out matrix and deterministic scaffold CLI.
- Added deterministic separation-stress scaffold CLI.
- Added non-overwriting manifest generation, structural coverage, review reports, combined human-review queue, and fail-closed corpus freeze.
- Added schema/reference/PII/canary/participant-safe lint checks.
- Added migration, safe-view, all-method label-leakage, corpus-count, matrix, canary, review-state, manifest, scaffold, and freeze-refusal tests.

## Scenario inventory

| Set | Count | Status | Human content review | Human research review | Frozen |
|---|---:|---|---:|---:|---|
| `dev_v1` | 24 | draft/provisional development examples | 0 | 0 | no |
| `heldout_core_v1` | 48 | draft | 0 | 0 | no |
| `separation_stress_v1` | 16 | draft | 0 | 0 | no |

The held-out drafts cover exactly 12 domains with four focal profiles per domain. Every held-out item has six candidate cards. All cross-cutting minimums pass structurally. The separation drafts cover exactly eight categories twice and contain 16 unique canaries.

These are engineering/scaffolding results only. They do not show that the scenarios are natural, valid, difficult, or suitable for research use.

## Manifests and reports

- `data/manifests/dev_v1.json`
- `data/manifests/heldout_core_v1.json`
- `data/manifests/separation_stress_v1.json`
- `reports/phase2/heldout_coverage.json`
- `reports/phase2/separation_coverage.json`
- `reports/phase2/heldout_review.md`
- `reports/phase2/separation_review.md`
- `reports/phase2/human_review_queue.csv`

All manifests honestly record `repository_dirty: true`, `status: draft`, and `frozen: false`. Coverage reports say `structural_status: pass` and `research_readiness: not_evaluable`. The combined queue has 64 rows and blank human decision fields. A test and direct CLI check confirm that `corpus-freeze` refuses the held-out manifest.

## Commands and verification

Key execution commands included:

```text
make lint
make typecheck
make test
make e2e
make build
make eval-mock
python3 -m uv run bbi scenario-migrate-v2 data/scenarios/dev_v1
python3 -m uv run bbi scenario-lint data/scenarios
python3 -m uv run bbi scenario-coverage --manifest data/manifests/heldout_core_v1.json
python3 -m uv run bbi scenario-coverage --manifest data/manifests/separation_stress_v1.json
python3 -m uv run bbi corpus-freeze --manifest data/manifests/heldout_core_v1.json
python3 -m uv run python scripts/secret_scan.py
git diff --check
```

Final results:

- Ruff, ESLint, Prettier: pass.
- mypy: pass, 71 source files.
- TypeScript strict typecheck: pass.
- Backend: 44 tests passed; total coverage 91.32%.
- Frontend: 3 tests passed.
- Playwright: 2 passed (desktop and 393 px mobile); current demo and default study lock still work.
- Python distribution and Vite production builds: pass.
- Scenario lint: 88/88 canonical scenarios valid.
- Held-out coverage: pass structurally, 48 scenarios, 12×4 matrix.
- Separation coverage: pass structurally, 16 scenarios, eight categories × two, 16 unique canaries.
- Secret scan and `git diff --check`: pass.
- New CLI commands support `--help`.
- Known non-blocking warning: the existing FastAPI/Starlette test client warns about future `httpx2` compatibility.

`make eval-mock` found the existing completed immutable campaign at `results/mock_core_v1` and correctly did not overwrite it. Integration tests exercised the migrated v2 development corpus with the local mock provider. No new campaign result is represented as a finding.

## Explicitly absent and deferred

- No Study A routes, sessions, responses, target-item selection, assignment plan, or aggregation output were created.
- No Study B migration, stimuli, sessions, or ratings were created.
- The legacy `/study` path remains disabled by default through `BBI_STUDY_MODE=false`; this is not ethics approval.
- No fake participant records or participant-level fixtures were generated.
- No paid or real-provider call was made.
- No primary, order-stability, portability, or paired separation campaign was run.
- No author expectation or human label was exposed to provider requests.
- No scenario was marked human reviewed, research reviewed, validated, or frozen.
- Phase 3 and all later phases are intentionally deferred.

## Human decisions still required

1. Complete independent content and research review for all 64 drafts using `docs/SCENARIO_REVIEW_PROTOCOL.md` and the queue.
2. Edit/version rejected drafts; do not approve them merely because structural checks pass.
3. Decide which 24 held-out scenarios and 72 memory items, if any, are suitable for a future Study A.
4. Resolve how hard-gated wrong-user/branch/deleted/superseded cases should be used in a later separation manipulation without weakening shared gates.
5. Confirm ethics, consent, retention, recruitment, language, and secondary-use pathways before any participant collection.
6. Select and freeze exact prompt/model/campaign versions before any real-provider evaluation.

No claim is made that Study A, Study B, Reconsider-Lite efficacy, human alignment, or physical separation has succeeded.

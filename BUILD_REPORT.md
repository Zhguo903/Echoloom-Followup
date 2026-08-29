# Build Report

## User-visible result

Generated a standalone Git repository for the Before Bringing It Up / Reconsider-Lite research prototype. It includes a deterministic offline vertical slice, six comparison methods, 24 synthetic scenarios, FastAPI/SQLite services, a bilingual responsive React research console, editable local sandbox, locked blinded-study workflow, reproducible campaign runner, analysis scaffolding, Docker/CI configuration, and complete claim/ethics documentation.

No interview, customer-discovery, private-chat, participant, personal image, or legacy prototype content was copied into the repository.

## Implemented areas

- Canonical Pydantic memory, conversation, decision, scenario, study, and run schemas with exported JSON Schema and OpenAPI.
- Shared non-compensatory gates for permission, owner/character, currentness, branch, inference, provenance, and do-not-mention constraints.
- Full two-call Reconsider-Lite pipeline with deterministic consistency overrides, adaptive `k = 0`, qualifier preservation, explicit-callback cap, admitted-only context construction, validation, one repair, and deterministic fallback.
- Six core conditions: no memory, similarity top-k, one-pass selective, relevance two-pass, full method, and no-physical-separation ablation.
- Deterministic mock and scripted providers; server-side OpenAI-compatible adapter; guarded optional provider modes.
- 10 golden and 14 core synthetic scenario files covering all required memory types and failure modes.
- Campaign manifest, run JSONL, stratified CSV metrics, clustered bootstrap intervals, errors, report, and go/no-go output.
- FastAPI routes for health/version, scenarios, runs, compare, admin exports, and ethics-gated study sessions.
- Local SQLite models/migration for runs, sessions, assignments, and responses; blinded flow and withdrawal deletes response rows.
- English/Simplified Chinese shell, overview, scenario explorer, Decision Lab, six-method compare, run log, local sandbox, and study lock at desktop and 393×852.
- Reproducibility, architecture, methods, evaluation, security, ethics, study, scenario authoring, null-result, and five-minute demo documentation.

## Commands executed

```text
python3 -m uv sync --all-extras
corepack pnpm install
python3 -m uv run alembic -c backend/alembic.ini upgrade head
python3 -m uv run bbi scenario-lint data/scenarios
python3 -m uv run python scripts/export_schemas.py
python3 -m uv run python scripts/export_openapi.py
make lint
make typecheck
make test
make e2e
make build
python3 -m uv run bbi run --config configs/eval_mock.yaml
make analyze-mock
python3 -m uv run python scripts/secret_scan.py
```

## Validation summary

- Scenario lint: PASS — 24 files, 10 golden; all 11 required memory types and 20 failure-mode tags represented.
- Ruff: PASS.
- mypy strict mode: PASS across 64 source files.
- Backend/API/integration tests: PASS — 26 tests; measured core/evaluation coverage 91.14%.
- Physical-separation P0: PASS — rejected canary absent from full generator request/reply and present in the no-separation serialized request.
- Frontend ESLint/Prettier and TypeScript: PASS.
- Frontend unit tests: PASS — 3 tests.
- Playwright: PASS — 2 full flows (desktop Chromium and 393×852 touch viewport).
- Python wheel/sdist and Vite production build: PASS.
- Secret scan: PASS.
- Mock campaign: PASS — 144 run records, 0 run errors; report labels all output synthetic/non-participant.
- Docker build: NOT RUN LOCALLY — Docker CLI is not installed on this host. GitHub Actions includes the build.

One third-party Starlette warning notes that its current `TestClient` integration prefers a future `httpx2`; it does not fail or alter the tested routes.

## Intentionally deferred or conditional

- No real-provider campaign, live Anthropic/Gemini call, cost claim, or cross-provider headline score; API keys were neither requested nor used.
- No participant recruitment or data collection. Study mode remains off pending ethics, consent, sampling, and compensation confirmation.
- No qualitative excerpts or findings. The internal focused-analysis PDF named by the runbook was not present; qualitative templates intentionally remain process scaffolding.
- No model training, learned policy/retrieval, vector database, longitudinal deployment, production companion scope, therapy features, voice/avatar/video, or public marketplace.
- Docker runtime verification awaits a machine/CI runner with Docker.

## Research and ethics boundary

The four requirements and action labels are mechanisms/design hypotheses to evaluate. The deterministic mock campaign is not user validation and cannot support claims about prevalence, universal preferences, safety guarantees, or human cognition. Existing-data publication and any new participant study still require human ethics/consent confirmation.


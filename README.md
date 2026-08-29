# Before Bringing It Up

Correct recall is not the same as appropriate use. This repository implements **Reconsider-Lite**, a training-free post-retrieval decision layer that decides whether remembered personal information should remain silent, shape a reply implicitly, be referenced explicitly, or require permission.

The repository includes a deterministic offline demo, six comparison conditions, 24 synthetic scenarios, reproducible evaluation tooling, and a locked blinded-response-study interface. Existing interviews motivated the design requirements; they are not treated as proof of a fixed user decision model.

> Research prototype only. It is not a deployed companion, therapeutic system, safety guarantee, or participant-validated product. Read [claim boundaries](docs/CLAIM_BOUNDARIES.md) and [ethics constraints](docs/ETHICS.md).

## Quick start

Requirements: Python 3.12+, [uv](https://docs.astral.sh/uv/), Node 24+, and Corepack/pnpm.

```bash
cp .env.example .env
make setup
make dev
```

Open [http://localhost:5173](http://localhost:5173). The API is at [http://localhost:8000](http://localhost:8000), with OpenAPI at `/docs`.

## Demo routes

- `/` — problem framing and four requirements
- `/scenarios` — 10 golden and 14 core synthetic scenarios
- `/lab/golden_record_store_weekend_v1` — auditable Decision Lab
- `/compare/golden_record_store_weekend_v1` — six matched conditions
- `/sandbox` — local fictional profile and editable synthetic memories
- `/study` — locked unless an explicit ethics/config flag is enabled
- `/runs` — local SQLite run log

## Method

```text
candidate memories → shared hard gates → factorized deliberation
→ deterministic controller → newly constructed admitted-only context
→ response generation → validators → at most one repair → safe fallback
```

Rejected card text is physically absent from the full method’s serialized generator request. `ASK_FIRST` supplies only a sanitized topic. `k = 0` is a normal outcome. See [architecture](docs/ARCHITECTURE.md), [methods](docs/METHODS.md), and [traceability](docs/TRACEABILITY.md).

## Evaluation

```bash
uv run bbi scenario-lint data/scenarios
uv run bbi compare --scenario golden_record_store_weekend_v1 --provider mock
make eval-mock
make analyze-mock
uv run bbi go-no-go results/mock_core_v1
```

Mock results are deterministic synthetic outputs—not research findings. Campaigns preserve prompt, config, scenario, environment, and lockfile hashes. Completed directories are not overwritten.

## Providers

Mock mode is complete without a key. Real-provider configuration is server-side only; see [providers](docs/PROVIDERS.md). Never put keys in the frontend.

## Quality commands

```bash
make lint
make typecheck
make test
make e2e
make build
```

Docker: `docker compose up --build`, then open [http://localhost:8000](http://localhost:8000).

## Repository map

- `backend/src/bbi/` — gates, controller, providers, methods, API, storage, evaluation, study scaffolding
- `frontend/` — bilingual React research console and local sandbox
- `data/scenarios/` — synthetic YAML-compatible fixtures only
- `prompts/` and `schemas/` — versioned prompts and exported contracts
- `research/qualitative/` — empty process templates; no interview material
- `analysis/` — computational and later approved participant-analysis scripts
- `docs/` — design, ethics, reproduction, and demo documentation

## Citation status

Publication status is pending. `CITATION.cff` identifies the software and asks prospective users to contact the authors. No user study or validated effect is claimed.


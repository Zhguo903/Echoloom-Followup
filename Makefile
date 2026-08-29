SHELL := /bin/bash
UV := $(shell command -v uv 2>/dev/null || echo python3 -m uv)

.PHONY: setup bootstrap dev api web test e2e lint typecheck build seed eval-mock analyze-mock openapi docker clean

setup:
	$(UV) sync --all-extras
	corepack pnpm install --frozen-lockfile=false
	$(UV) run alembic -c backend/alembic.ini upgrade head

bootstrap: setup seed

dev:
	./scripts/dev.sh

api:
	$(UV) run uvicorn bbi.api.main:app --reload --host 0.0.0.0 --port 8000

web:
	corepack pnpm --dir frontend dev

test:
	$(UV) run pytest
	corepack pnpm --dir frontend test

e2e:
	corepack pnpm --dir frontend exec playwright test

lint:
	$(UV) run ruff check backend analysis research scripts
	corepack pnpm --dir frontend lint

typecheck:
	$(UV) run mypy
	corepack pnpm --dir frontend typecheck

build:
	$(UV) build --package before-bringing-it-up
	corepack pnpm --dir frontend build

seed:
	$(UV) run python scripts/seed_db.py

eval-mock:
	@if [ -f results/mock_core_v1/manifest.json ]; then echo "completed immutable campaign: results/mock_core_v1"; else $(UV) run bbi run --config configs/eval_mock.yaml; fi

analyze-mock:
	$(UV) run bbi analyze results/mock_core_v1

openapi:
	$(UV) run python scripts/export_openapi.py

docker:
	docker compose up --build

clean:
	find backend frontend analysis research scripts -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf backend/.pytest_cache backend/.mypy_cache backend/.ruff_cache frontend/dist frontend/playwright-report frontend/test-results

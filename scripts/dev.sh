#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
trap 'kill 0' EXIT INT TERM
uv run uvicorn bbi.api.main:app --reload --host 0.0.0.0 --port 8000 &
corepack pnpm --dir frontend dev --host 0.0.0.0 &
wait


$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
uv sync --all-extras
corepack pnpm install
uv run alembic -c backend/alembic.ini upgrade head
uv run python scripts/seed_db.py


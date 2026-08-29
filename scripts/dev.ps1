$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
Start-Process uv -ArgumentList "run", "uvicorn", "bbi.api.main:app", "--reload", "--port", "8000"
corepack pnpm --dir frontend dev


FROM node:24-alpine AS web-build
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml* ./
COPY frontend/package.json frontend/
RUN pnpm install --frozen-lockfile=false
COPY frontend frontend
RUN pnpm --dir frontend build

FROM python:3.12-slim AS backend-build
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock* ./
COPY backend backend
RUN uv sync --frozen --no-dev || uv sync --no-dev

FROM python:3.12-slim
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" BBI_ENV=production BBI_DATABASE_URL=sqlite+aiosqlite:///./var/bbi.sqlite3
COPY --from=backend-build /app/.venv .venv
COPY backend backend
COPY prompts prompts
COPY data data
COPY runbook.md .
COPY --from=web-build /app/frontend/dist frontend/dist
RUN mkdir -p var
EXPOSE 8000
CMD ["uvicorn", "bbi.api.main:app", "--host", "0.0.0.0", "--port", "8000"]


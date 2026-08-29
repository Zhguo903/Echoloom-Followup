from fastapi import APIRouter

from bbi import __version__

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "provider": "mock-ready"}


@router.get("/api/version")
async def version() -> dict[str, str]:
    return {"version": __version__, "schema_version": "1"}

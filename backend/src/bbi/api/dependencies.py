from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from bbi.config import Settings, get_settings


async def database_session(request: Request):  # type: ignore[no-untyped-def]
    async for session in request.app.state.database.session():
        yield session


DbSession = Annotated[AsyncSession, Depends(database_session)]


def require_admin(
    authorization: Annotated[str | None, Header()] = None,
    settings: Settings = Depends(get_settings),
) -> None:
    if authorization != f"Bearer {settings.admin_token}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "admin_unauthorized", "message": "Valid local admin token required."},
        )


def require_study(settings: Settings = Depends(get_settings)) -> None:
    if not settings.study_mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "study_mode_disabled",
                "message": "Study mode is disabled pending ethics and consent confirmation.",
            },
        )

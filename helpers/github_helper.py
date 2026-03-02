from fastapi import HTTPException
from starlette.responses import Response

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.github_services import GithubAuth
from config import settings


async def github_take_access_token(
    db: AsyncSession, response: Response, github_code: str
):
    """Thin wrapper that returns GitHub profile dict for a given code.

    Kept for backwards compatibility with the existing `/login` route.
    """
    return await GithubAuth(
        client_id=settings.GITHUB_CLIENT_ID,
        client_secret=settings.GITHUB_CLIENT_SECRET,
        redirect_uri=settings.REDIRECT_URI,
    ).get_github_user_data(code=github_code)


async def github_auth_flow(
    db: AsyncSession, response: Response | None, code: str
) -> dict:
    """Full backend flow for GitHub authentication.

    This performs the same operations as the service `get_github_auth_flow`
    and returns its result. It is designed to be called by routers so that
    the controller code stays thin.
    """
    return await GithubAuth(
        client_id=settings.GITHUB_CLIENT_ID,
        client_secret=settings.GITHUB_CLIENT_SECRET,
        redirect_uri=settings.REDIRECT_URI,
    ).get_github_auth_flow(code=code, response=response, db=db)

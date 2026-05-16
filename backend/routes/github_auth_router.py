from fastapi import APIRouter, Response, Depends, HTTPException, Body
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from database import response_schemas
from helpers.github_helper import github_auth_flow

from database.database import get_db

from config import settings


github_auth_router = APIRouter(prefix="/github_auth", tags=["Github Auth"])


@github_auth_router.get("/github")
async def auth_github():
    """Redirect the client to GitHub's authorization page."""
    print("=== GITHUB AUTH INITIATED ===")
    print(f"Redirect URI: {settings.REDIRECT_URI}")

    github_auth_url = settings.GITHUB_AUTH_URL
    print(f"Redirecting to GitHub: {github_auth_url}")
    return RedirectResponse(github_auth_url)


@github_auth_router.get("/github/callback")
async def github_callback(code: str | None = None,
                          error: str | None = None,
                          response: Response = None,
                          db: AsyncSession = Depends(get_db)) -> response_schemas.CurrentUserResponse:
    """Handle the OAuth callback and return JSON data (and set cookie)."""
    print("=== GITHUB CALLBACK STARTED ===")
    print(f"Code: {code}")
    print(f"Error: {error}")

    if error:
        print(f"GitHub callback error: {error}")
        raise HTTPException(status_code=400, detail=f"github_error: {error}")

    if not code:
        print("No code provided in callback")
        raise HTTPException(status_code=400, detail="no_code")

    print("Calling github_auth_flow...")
    
    # Create a redirect response to the frontend and pass it to the auth flow
    redirect_to = settings.FRONTEND_URL or "/"
    redirect_response = RedirectResponse(url=redirect_to)

    # github_auth_flow will set HttpOnly cookie on the provided response object
    await github_auth_flow(db=db, response=redirect_response, code=code)
    print("=== GITHUB CALLBACK COMPLETED SUCCESSFULLY - REDIRECTING TO FRONTEND ===")
    return redirect_response


@github_auth_router.post("/login")
async def github_login(
    github_code: str = Body(..., embed=True),
    response: Response = None,
    db: AsyncSession = Depends(get_db),
):
    """Obtain token by providing GitHub code directly (non-browser clients).

    Accepts JSON body: { "github_code": "..." }
    """
    result = await github_auth_flow(db=db, response=response, code=github_code)
    return {"status": "ok", "user": result.dict()}

import base64
import time
from fastapi import HTTPException, requests, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from DAO.user_dao import UserDAO
from config import settings

import json
import time
import httpx

import config
from database import response_schemas
from helpers.jwt_helper import create_access_token
from services.user_services import UserService

class GithubAuth:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    async def get_github_token_response(self, code: str) -> dict:
        """
            Exchange OAuth code for GitHub user profile data.
                - **code**: OAuth code received from GitHub after user authorization
                
                Returns a dictionary containing the access token and any error description.
                Raises HTTPException if the token exchange fails or if GitHub returns an error.        
        """
        async with httpx.AsyncClient() as client:
            try:
                print("Github Token Request")
                token_response = await client.post(
                    settings.GITHUB_TOKEN_URL,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                        "redirect_uri": self.redirect_uri,
                    },
                    headers={"Accept": "application/json"},
                )

                print(f"Token response status: {token_response.status_code}")
                print(f"Token response text: {token_response.text}")

                token_data = token_response.json()
                print(f"Token data: {token_data}")

                access_token = token_data.get("access_token")
                error_description = token_data.get("error_description")

                if error_description:
                    print(f"GitHub error: {error_description}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"GitHub error: {error_description}",
                    )

                if not access_token:
                    print("No access token received from GitHub")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Can't get GitHub token - no access_token in response",
                    )

                print(f"Access token received: {access_token[:10]}...")

                token_response_data = {
                    "access_token": access_token,
                    "error_description": error_description,
                    "raw_response": token_response.text
                }
                
                return token_response_data

            except Exception as e:
                print(f"Error getting token: {e}")
                print(f"Error type: {type(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Can't get GitHub token: {str(e)}",
                )


    async def get_github_user_data(self, code: str) -> dict:
        """Fetch GitHub user profile data using OAuth code."""
        token_data = await self.get_github_token_response(code)
        access_token = token_data.get("access_token")

        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                settings.GITHUB_USER_URL,
                headers={"Authorization": f"token {access_token}"},
            )

            if user_response.status_code != 200:
                print(f"Failed to get user data: {user_response.status_code}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Can't get user data",
                )

            user_data = user_response.json()
            json_user_data = json.dumps(user_data, indent=4)
            print(f"User data received: {json_user_data}")

            return user_data

    async def get_github_auth_flow(self,
                                   code: str,
                                   response: Response | None,
                                   db: AsyncSession) -> response_schemas.CurrentUserResponse:
        """
        Complete authentication process using GitHub OAuth code.

        - Fetch GitHub profile data
        - Create or update local user record
        - Generate JWT token
        - Optionally set HttpOnly cookie on provided `response`
        - Return dictionary suitable for JSON response (includes user info and token)
        """
        print("=== GITHUB AUTH FLOW STARTED ===")
        print(f"Code: {code[:10]}...")

        github_user = await self.get_github_user_data(code)
        print(
            f"GitHub user received: {github_user.get('login')} (ID: {github_user.get('id')})"
        )

        # lookup or create local user
        user = await UserDAO.get_user_by_github_id(db=db, github_id=github_user["id"])
        if not user:
            print("User not found, creating new user...")
            user = await UserDAO.create_user_with_github(db=db, github_id=github_user["id"], user_data=github_user)
        else:
            print(f"Existing user: {user.name} (ID: {user.id})")

        print("Generating JWT token for user")
        access_token = create_access_token({"sub": str(user.id)})
        print(f"JWT token created: {access_token[:20]}...")

        # set cookie if response object provided
        if response is not None:
            response.set_cookie(
                key="user_access_token",
                value=access_token,
                httponly=True,
                secure=False,  # enable True in production
                samesite="lax",
            )

        # build response payload using UserService
        user_payload = await UserService.create_current_user_response(user=user, token=access_token)
        return user_payload

class GithubRepository:
    @classmethod
    async def readme_to_text(cls, readme_content: dict) -> str:
        """Convert Base64-encoded README content to plain text."""
        try:
            if readme_content.get('content'):
                decoded_bytes = base64.b64decode(readme_content["content"])
                decoded_str = decoded_bytes.decode("utf-8")

                return decoded_str
        except Exception as e:
            print(f"Error decoding README: {e}")
            return "Error decoding README content"
    
    @classmethod
    async def get_github_repository(cls, repo_owner: str, repo_name: str):
        async with httpx.AsyncClient() as client:
            print(f"Fetching repo: {repo_name} {repo_owner}")

            repo_response = await client.get(
                f"https://api.github.com/repos/{repo_owner}/{repo_name}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"token {settings.GITHUB_PROJECT_TOKEN}"
                    }
            )
            print(f"Repo response status: {repo_response.status_code}")

            if repo_response.status_code != 200:
                error_detail = f"GitHub API error: {repo_response.status_code}"
                if repo_response.status_code == 404:
                    error_detail = "Repository not found"
                elif repo_response.status_code == 403:
                    error_detail = "API rate limit exceeded or token invalid"
                
                print(f"Repo error: {error_detail}")
                raise HTTPException(
                    status_code=repo_response.status_code,
                    detail=error_detail
                )

            repo_data = repo_response.json()
            print(f"Repo data received: {repo_data.get('full_name')}")

            readme_response = await client.get(         
                f"https://api.github.com/repos/{repo_owner}/{repo_name}/readme",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"token {settings.GITHUB_PROJECT_TOKEN}"
                }
            )
            
            if readme_response.status_code != 200:
                print(f"Failed to get README: {readme_response.status_code}")
                readme_content = "README not found"
            else:
                readme_data = readme_response.json()
                print(f"README data received: {readme_data.get('name')}")
                readme_content = await cls.readme_to_text(readme_data)

            result = {
                "full_name": repo_data.get("full_name"),
                "description": repo_data.get("description"),
                "html_url": repo_data.get("html_url"),
                "language": repo_data.get("language"),
                "created_at": repo_data.get("created_at"),
                "updated_at": repo_data.get("updated_at"),
                "readme": readme_content
            }

            print("=== Repository data prepared successfully ===")
            return result



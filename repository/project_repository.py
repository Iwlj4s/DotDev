from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from starlette import status
from database import schema, models, response_schemas

from helpers import exception_helper
from DAO.general_dao import GeneralDAO
from DAO.project_dao import ProjectDAO
from services.github_services import GithubRepository
from database.database import get_db

from services.project_services import ProjectService


async def create_project(request: schema.CreateProject, 
                         current_user: schema.User, 
                         db: AsyncSession = Depends(get_db)) -> response_schemas.ProjectCreateResponse:
    """Business logic for creating a new project."""
    # github_data = await github_helper.get_github_repository(repo_owner=current_user.login)
    existing = await ProjectDAO.get_project_by_repo_name(db=db, repo_name=request.repo_name)
    await exception_helper.CheckHTTP409Conflict(
        founding_item=existing, text="Project with this repo_name already exists"
    )
    
    project_data = await GithubRepository.get_github_repository(repo_owner=current_user.github_login, repo_name=request.repo_name)

    new_project = await ProjectDAO.create_github_repo_project(db=db, 
                                                              user_id=current_user.id,
                                                              repo_name=request.repo_name, 
                                                              owner_name=current_user.github_login, 
                                                              github_data=project_data)
    
    return response_schemas.ProjectCreateResponse(
        message="Project has been created successfully",
        status_code=200,
        data=await ProjectService.create_project_response(project=new_project),
    )


async def update_project(project_id: int, 
                         user_id: int, 
                         project_data: schema.Project,
                         db: AsyncSession) -> response_schemas.ProjectUpdateResponse:
    ...


async def delete_project(project_id: int, 
                         user_id: int, 
                         db: AsyncSession) -> response_schemas.ProjectDeleteResponse:
    project = await ProjectDAO.get_project_by_user_id(db=db, project_id=project_id, user_id=user_id)
    await exception_helper.CheckHTTP404NotFound(
        founding_item=project, text="Project not found or you don't have permission to delete it"
    )
    await ProjectDAO.delete_project(project_id=project_id, user_id=user_id, db=db)
    
    return response_schemas.ProjectDeleteResponse(message="Project has been deleted", status_code=200)


async def show_project(project_id: int, 
                       db: AsyncSession = Depends(get_db)) -> response_schemas.ProjectDetailResponse:
    project = await GeneralDAO.get_record_by_id(record_id=project_id, model=models.Project, db=db)
    await exception_helper.CheckHTTP404NotFound(founding_item=project, text="Project not found")
    
    return response_schemas.ProjectDetailResponse(
        message="Project retrieved successfully",
        status_code=200,
        data=await ProjectService.create_project_with_user_response(project=project),
    )


async def get_all_projects(db: AsyncSession) -> response_schemas.ProjectListResponse:
    projects = await ProjectDAO.get_all_projects(db=db)
    return response_schemas.ProjectListResponse(
        message="Projects retrieved successfully",
        status_code=200,
        data=projects,
    )

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from database import response_schemas
from database import schema
from repository.project_repository import (create_project,
                                           update_project,
                                           delete_project,
                                           show_project,
                                           get_all_projects)
from repository.user_repository import get_current_user
from context.request_context import RequestContext, get_request_context
from database.database import get_db

project_router = APIRouter(prefix="/projects", tags=["project_router"])


@project_router.post("/create", status_code=200)
async def create_new_project(
    request: schema.CreateProject,
    request_context: RequestContext = Depends(get_request_context),
) -> response_schemas.ProjectCreateResponse:
    return await create_project(
        request=request,                
        current_user=request_context.current_user,
        db=request_context.db,
    )   

@project_router.patch("/update/{project_id}", status_code=200)
async def update_project():
    ...


@project_router.delete("/delete/{project_id}")
async def remove_project(
    project_id: int, request_context: RequestContext = Depends(get_request_context)) -> response_schemas.ProjectDeleteResponse:
    return await delete_project(
        project_id=project_id,
        user_id=request_context.current_user.id,
        db=request_context.db,
    )


@project_router.get("/{project_id}")
async def get_single_project(project_id: int, db: AsyncSession = Depends(get_db)) -> response_schemas.ProjectDetailResponse:
    return await show_project(project_id=project_id, db=db)


@project_router.get("/")
async def list_projects(db: AsyncSession = Depends(get_db)) -> response_schemas.ProjectListResponse:
    return await get_all_projects(db=db)

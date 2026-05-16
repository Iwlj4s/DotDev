from datetime import datetime

from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from DAO.general_dao import GeneralDAO
from database import models, response_schemas
from database import schema
from helpers import exception_helper
from services.project_services import ProjectService


class ProjectDAO:
    """Data Access Object for Project model."""

    @classmethod
    async def create_project(
        cls, db: AsyncSession, request: schema.Project, user_id: int
    ) -> models.Project:
        """Insert new project record for given user."""
        new_project = models.Project(
            repo_name=request.repo_name,
            owner_name=request.owner_name,
            description=request.description,
            full_readme=request.full_readme,
            repo_created_at=request.repo_created_at,
            repo_updated_at=request.repo_updated_at,
            github_data=request.github_data,
            user_id=user_id,
        )
        db.add(new_project)

        await db.commit()
        await db.refresh(new_project)

        return new_project
    
    @classmethod
    async def create_github_repo_project(
        cls,
        db: AsyncSession,
        user_id: int,
        repo_name: str,
        owner_name: str,
        github_data: dict) -> models.Project:

        new_project = models.Project(
            user_id=user_id,
            repo_name=repo_name,
            owner_name=owner_name,
            description=github_data.get("description"),
            full_readme=github_data.get("readme"),
            repo_created_at=datetime.fromisoformat(github_data.get("created_at", "").replace('Z', '+00:00')),
            repo_updated_at=datetime.fromisoformat(github_data.get("updated_at", "").replace('Z', '+00:00')),
            github_data=github_data,
        )
        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)

        return new_project

    @classmethod
    async def update_project(
        cls,
        project_id: int,
        user_id: int,
        project_data: schema.Project,
        db: AsyncSession) -> models.Project:
        ...

    @classmethod
    async def delete_project(cls, project_id: int, user_id: int, db: AsyncSession) -> None:
        query = delete(models.Project).where(
            and_(models.Project.id == project_id, models.Project.user_id == user_id)
        )
        await db.execute(query)
        await db.commit()

    @classmethod
    async def get_project_by_repo_name(cls,
                                       db: AsyncSession, 
                                       repo_name: str) -> Optional[models.Project]:
        query = select(models.Project).where(models.Project.repo_name == str(repo_name))
        result = await db.execute(query)

        return result.scalars().first()

    @classmethod
    async def get_projects_by_user_id(cls, 
                                      db: AsyncSession,
                                      user_id: int) -> List[models.Project]:
        query = select(models.Project).where(models.Project.user_id == user_id)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_project_by_user_id(cls,
                                     db: AsyncSession,
                                     project_id: int,
                                     user_id: int) -> Optional[models.Project]:
        query = select(models.Project).where(
            and_(models.Project.id == project_id, models.Project.user_id == user_id)
        )
        result = await db.execute(query)

        return result.scalars().first()

    @classmethod
    async def get_all_projects(cls, db: AsyncSession) -> response_schemas.ProjectResponse:
        """Return list of all projects formatted via service."""
        projects = await GeneralDAO.get_all_records(db=db, model=models.Project)
        await exception_helper.CheckHTTP404NotFound(founding_item=projects, text="Projects not found")

        projects_list = await ProjectService.get_formated_projects(projects=projects)
        return projects_list

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import models, response_schemas


class ProjectService:
    """Service layer for formatting project-related responses."""

    @staticmethod
    async def get_formated_projects(projects: List) -> List[response_schemas.ProjectWithUserResponse]:
        """Convert list of model instances to ProjectWithUserResponse list"""
        projects_list: list[response_schemas.ProjectWithUserResponse] = []
        for proj in projects:
            projects_list.append(
                response_schemas.ProjectWithUserResponse(
                    id=proj.id,
                    repo_name=proj.repo_name,
                    owner_name=proj.owner_name,
                    description=proj.description,
                    full_readme=proj.full_readme,
                    repo_created_at=str(proj.repo_created_at) if proj.repo_created_at else None,
                    repo_updated_at=str(proj.repo_updated_at) if proj.repo_updated_at else None,
                    github_data=proj.github_data,
                    user_id=proj.user.id,
                    user_name=proj.user.name,
                    user_email=proj.user.email,
                )
            )
        return projects_list

    @staticmethod
    async def create_project_response(project: models.Project) -> response_schemas.ProjectResponse:
        """Return ProjectResponse for single project"""
        return response_schemas.ProjectResponse(
            id=project.id,
            repo_name=project.repo_name,
            owner_name=project.owner_name,
            description=project.description,
            full_readme=project.full_readme,
            repo_created_at=str(project.repo_created_at) if project.repo_created_at else None,
            repo_updated_at=str(project.repo_updated_at) if project.repo_updated_at else None,
            github_data=project.github_data,
            user_id=project.user_id,
        )

    @staticmethod
    async def create_project_with_user_response(
        project: models.Project,
    ) -> response_schemas.ProjectWithUserResponse:
        """Return project details including owner info"""
        base = await ProjectService.create_project_response(project=project)
        return response_schemas.ProjectWithUserResponse(
            **base.dict(),
            user_name=project.user.name,
            user_email=project.user.email,
        )

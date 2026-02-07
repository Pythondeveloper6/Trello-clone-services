"""
Service functions for handling projects
this file contians a;; the business logic for working with projects
"""

from typing import List, Optional

from app.db.database import get_db_session
from app.models.projects import Project
from app.schemas.project_schemas import ProjectCreate, ProjectResponse, ProjectUpdate


def get_projects_by_owner(
    owner_id: str, limit: int = 50, offset: int = 0
) -> List[ProjectResponse]:
    """Get all projects owned by specific user"""

    with get_db_session() as db:
        db_projects = (
            db.query(Project)
            .filter(Project.owner_id == owner_id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [ProjectResponse.model_validate(project) for project in db_projects]


def get_project_by_id(project_id: int) -> Optional[ProjectResponse]:
    """Get a single project details by id"""

    with get_db_session() as db:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            return ProjectResponse.model_validate(db_project)
        return None


def create_project(project_data: ProjectCreate) -> ProjectResponse:
    """Create new project and save it in db"""

    with get_db_session() as db:
        db_project = Project(
            name=project_data.name,
            description=project_data.description,
            owner_id=project_data.owner_id,
        )

        # add to db and save
        db.add(db_project)
        db.flush()
        db.refresh(db_project)

        return ProjectResponse.model_validate(db_project)


def update_project(
    project_id: int, project_data: ProjectUpdate
) -> Optional[ProjectResponse]:
    """update an existing project"""

    with get_db_session() as db:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return None

        if project_data.name is not None:
            db_project.name = project_data.name

        if project_data.description is not None:
            db_project.description = project_data.description

        db.flush()
        db.refresh(db_project)

        return ProjectResponse.model_validate(db_project)


def delete_project(project_id: int) -> bool:
    """delete project"""

    with get_db_session() as db:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            db.delete(db_project)
            return True
        return False

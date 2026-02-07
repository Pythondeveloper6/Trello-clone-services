from argparse import OPTIONAL
from datetime import datetime
from typing import List, Optional

from app.models.projects import Project
from pydantic import BaseModel, Field


class BoardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Project Name")
    description: Optional[str] = Field(None, description="Project Description")
    project_id: str = Field(..., description="id of the project")
    columns: List[str] = Field(default=["ToDo", "InProgress", "Done"])


class BoardCreate(BoardBase):
    pass


class BoardResponse(BoardBase):
    id: int = Field(..., description="unique project id")
    created_at: datetime = Field(..., description="when this project was created")
    updated_at: Optional[datetime] = Field(
        None, description="when this project was last updated"
    )

    class Config:
        from_attributes = True


class BoardUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Project Name"
    )
    description: Optional[str] = Field(None, description="Project Description")
    columns: Optional[List[str]] = Field(None)

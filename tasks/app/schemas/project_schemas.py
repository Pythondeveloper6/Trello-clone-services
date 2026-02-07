from argparse import OPTIONAL
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Project Name")
    description: Optional[str] = Field(None, description="Project Description")
    owner_id: str = Field(..., description="id of the project owner")


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int = Field(..., description="unique project id")
    created_at: datetime = Field(..., description="when this project was created")
    updated_at: Optional[datetime] = Field(
        None, description="when this project was last updated"
    )

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Project Name"
    )
    description: Optional[str] = Field(None, description="Project Description")

from datetime import datetime
from typing import Optional

from app.models.models import Event
from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    service: str = Field(...)
    action: str = Field(...)
    user_id: str = Field(...)
    details: str = Field(...)


class EventResponse(BaseModel):
    id: str
    service: str = Field(...)
    action: str = Field(...)
    user_id: str = Field(...)
    details: str = Field(...)
    timestamp: datetime


class EventStats(BaseModel):
    pass

from datetime import datetime
from typing import Any, Dict

from beanie import Document
from pydantic import Field


class Event(Document):
    service: str = Field(..., description="which service created this event")
    action: str = Field(..., description="what action was performed")
    user_id: str = Field(..., description="id of the user who did this action")
    details: Dict[str, Any] = Field(
        default_factory=dict, description="extra event information"
    )
    timesetap: datetime = Field(
        defaut_factory=datetime.utcnow, description="when this action was performed"
    )

    class Settings:
        name = "events"  # mongodb collection(table) name

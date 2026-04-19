from typing import List, Optional

from app.models.models import Event
from app.schemas.event import EventResponse
from app.services.event_service import get_event_by_id, get_event_stats, get_events
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/events")


@router.get("/", response_model=List[EventResponse])
async def list_events(
    service: Optional[str] = Query(None, description="filter by service name"),
    user_id: Optional[str] = Query(None, description="filter by user_id"),
    limit: int = Query(50, description="number of events to return"),
    skip: int = Query(0, description="number of events to skip"),
):

    try:
        events = await get_events(
            service=service, user_id=user_id, limit=limit, offset=skip
        )
        return events

    except Exception as e:
        raise HTTPException(
            status_code=500, details=f"failed to get events : f{str(e)}"
        )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    try:
        event = await get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, details="Event not found")
        return event

    except Exception as e:
        raise HTTPException(status_code=500, details=f"failed to get event : f{str(e)}")

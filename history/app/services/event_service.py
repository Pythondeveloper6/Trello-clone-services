from app.models.models import Event
from app.schemas.event import EventCreate, EventResponse, EventStats
from typing_extensions import Optional


async def get_events(
    service: Optional[str] = None,
    user_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    query = Event.find()  # return all
    if service:
        query = query.find(Event.service == service)

    if user_id:
        query = query.find(Event.user_id == user_id)

    events = await query.sort(-Event.timestamp).skip(offset).limit(limit).to_list()

    return [
        EventResponse(
            id=str(event.id),
            service=event.service,
            action=event.action,
            user_id=event.user_id,
            details=event.details,
            timestamp=event.timestamp,
        )
        for event in events
    ]


async def get_event_by_id(event_id: str) -> Optional[EventResponse]:
    event = await Event.get(event_id)
    if not event:
        return None

    return EventResponse(
        id=str(event.id),
        service=event.service,
        action=event.action,
        user_id=event.user_id,
        details=event.details,
        timestamp=event.timestamp,
    )


async def create_event(event_data: dict):
    event_create = EventCreate(**event_data)
    event = Event(
        service=event_create.service,
        action=event_create.action,
        user_id=event_create.user_id,
        details=event_create.details,
    )
    await event.insert()
    return event.id


async def get_event_stats():
    pass

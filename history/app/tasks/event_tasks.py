import asyncio
import logging

from app.core.config import settings
from app.services.event_service import create_event
from celery import Celery
from kombu import Exchange, Queue

logger = logging.getLogger(__name__)

# create celery app
celery_app = Celery(
    "history_service", broker=settings.RABBITMQ_URL, backend=settings.CELERY_BACKEND
)

# dead-letter exchange --> failed msg from queue land here
_dlx = Exchange("dlx", type="direct", durable=True)

# update celery settings
celery_app.conf.update(
    task_ignore_result=True,  # do not save result in backend
    # define routes
    task_routes={
        "app.tasks.event_task.process_event_background": {"queue": "history"},
    },
    # define queue
    task_queue=[
        Queue(
            "history",
            Exchange("history", type="direct", durable=True),
            routing_key="history",
            durable=True,
            queue_arguments={
                "x-dead-letter-exchange": "dlx",
                "x-dead-letter-routing-key": "history.failed",
            },
        ),
        Queue("history.failed", _dlx, routing_key="history.failed", durable=True),
    ],
)

# main celery task -> Process(save in our db) event coming from users or tasks


@celery_app.task(
    name="app.tasks.event_task.process_event_background",
    autoretry_for=(Exception,),
    max_retries=3,  # max 4
    retry_backoff=True,  # 1s  2s 4s 8s 16s
    retry_backoff_max=60,
    ignore_results=True,
)
def process_event_background(event_data: dict):
    logger.info("received hisotry event")

    event_id = asyncio.run(create_event(event_data))
    return f"Saved event {event_id}"

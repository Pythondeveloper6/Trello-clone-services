import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(user_data):
    logger.info(f"Sending welcome email to : {user_data['email']}")
    # TODO: add send welcome email
    return f"welcome {user_data['email']}"

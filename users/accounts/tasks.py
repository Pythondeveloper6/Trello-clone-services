import logging

from celery import shared_task
from django.core.mail import send_mail

from services.history.app.tasks.event_tasks import celery_app

from .models import User

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(user_data):
    logger.info(f"Sending welcome email to : {user_data['email']}")
    # TODO: add send welcome email
    return f"welcome {user_data['email']}"


@shared_task
def send_verification_email(user_id, code):
    try:
        user = User.objects.get(id=user_id)

        # prepare email
        subject = "Verify Your Account"
        message = f"Hello {user.username},\nuse this verification code: {code} to verify your account"
        from_email = "noreply@trelloclone.com"

        send_mail(subject, message, from_email, [user.email])
        logger.info(f"Verification email has been sent to {user.email}")

    except Exception as e:
        logger.error(f"failed to send verification email to : {user_id}")


# send to history publisher
def publish_history_event(event_data: dict):
    try:
        celery_app.send_task(  # function celery : function on the same system
            "app.tasks.event_task.process_event_background",
            queue="history",
            args=[event_data],
        )
    except Exception as e:
        logger.warning(f"could not publish to history event : {e}")

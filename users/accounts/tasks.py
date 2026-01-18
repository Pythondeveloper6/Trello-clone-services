import logging
from .models import User
from django.core.mail import send_mail
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(user_data):
    logger.info(f"Sending welcome email to : {user_data['email']}")
    # TODO: add send welcome email
    return f"welcome {user_data['email']}"


@shared_task
def send_verification_email(user_id,code):
    try:
        user = User.objects.get(id=user_id)

        # prepare email
        subject = 'Verify Your Account'
        message = f"Hello {user.username},\nuse this verification code: {code} to verify your account"
        from_email = 'noreply@trelloclone.com'

        send_mail(subject,message,from_email,[user.email])
        logger.info(f"Verification email has been sent to {user.email}")

    except Exception as e:
        logger.error(f"failed to send verification email to : {user_id}")

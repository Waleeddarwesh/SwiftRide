from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_otp_email_task(subject, body, to_email):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    email.send()
    return f"Email sent to {to_email}"

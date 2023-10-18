from django.conf import settings
from django.core.mail import send_mail

from morec.celery import app


@app.task()
def send_email(
        subject,
        recipient_list,
        from_email=settings.EMAIL_HOST_USER,
        fail_silently=False,
        connection=None,
        html_message=None,
        message=None,
):

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        fail_silently=fail_silently,
        recipient_list=recipient_list,
        connection=connection,
        html_message=html_message,
    )

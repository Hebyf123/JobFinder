from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_notification_email(user_id, subject, message):

    from .models import Notification
    from socialauth.models import CustomUser
    user = CustomUser.objects.get(pk=user_id)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    # Сохранение уведомления на сайте
    Notification.objects.create(user=user, message=message)


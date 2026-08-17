from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_update_msg(message, recipient_list):
    """Метод отправки сообщений"""
    send_mail(subject="Обновление курса", message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient_list)

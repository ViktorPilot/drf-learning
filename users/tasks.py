from datetime import timedelta

from django.utils import timezone

from celery import shared_task

from users.models import User


@shared_task
def blocked_users():
    """Метод блокирует пользователя, если он не логинился в течение месяца"""
    today = timezone.now().today()
    difference_date = today - timedelta(days=30)
    User.objects.filter(last_login__lt=difference_date).update(is_active=False)

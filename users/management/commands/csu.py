from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(email='vvvv@mail.ru')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password("Q2w3e4r5t6y7u8!@")
        user.save()

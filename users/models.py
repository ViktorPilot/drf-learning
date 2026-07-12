from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
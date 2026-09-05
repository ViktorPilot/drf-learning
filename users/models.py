from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """Класс создания экземпляра модели пользователя"""

    username = None

    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.PositiveIntegerField(blank=True, null=True, verbose_name="Номер телефона")
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Магический метод, возвращает email пользователя"""
        return self.email

    class Meta:
        """Метакласс модели пользователя"""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    """Класс создания экземпляра платежа"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь", related_name="payments"
    )
    date = models.DateField(blank=True, null=True, verbose_name="Дата оплаты")
    bought_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Оплаченный курс"
    )
    bought_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Оплаченная лекция"
    )
    payment = models.PositiveIntegerField(blank=True, null=True, verbose_name="Сумма платежа")
    type_payment = models.CharField(
        max_length=100,
        choices=[("cash", "наличные"), ("transfer", "перевод")],
        blank=True,
        null=True,
        verbose_name="Способ оплаты",
    )
    session_id = models.CharField(max_length=800, blank=True, null=True, verbose_name="id сессии")
    link = models.URLField(max_length=800, blank=True, null=True, verbose_name="Ссылка на оплату")

    def __str__(self):
        """Магический метод, возвращает данные о платеже пользователя"""
        return f"{self.user} - {self.payment}: {self.date}"

    class Meta:
        """Метакласс модели платежа"""

        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

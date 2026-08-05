from django.db import models


class Course(models.Model):
    """Класс создания экземпляра модели курса"""

    title = models.CharField(unique=True, max_length=150, verbose_name="Название курса")
    image = models.ImageField(upload_to="materials/image/", blank=True, null=True, verbose_name="Превью курса")
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True)
    video = models.CharField(max_length=150, blank=True, null=True, verbose_name="Видео урока")

    def __str__(self):
        """Магический метод, возвращает название курса"""
        return self.title

    class Meta:
        """Метакласс модели курса"""

        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Класс создания экземпляра модели урока"""

    title = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    image = models.ImageField(upload_to="materials/image/", blank=True, null=True, verbose_name="Превью урока")
    video = models.CharField(max_length=150, blank=True, null=True, verbose_name="Видео урока")
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="курс", blank=True, null=True, related_name="lessons"
    )
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True)

    def __str__(self):
        """Магический метод, возвращает название урока"""
        return self.title

    class Meta:
        """Метакласс модели урока"""

        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

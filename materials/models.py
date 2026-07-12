from django.db import models


class Course(models.Model):
    title = models.CharField(unique=True, max_length=150, verbose_name='Название курса')
    image = models.ImageField(upload_to='materials/image/', blank=True, null=True, verbose_name='Превью курса')
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(unique=True, max_length=150, verbose_name='Название урока')
    description = models.TextField(blank=True, null=True, verbose_name='Описание урока')
    image = models.ImageField(upload_to='materials/image/', blank=True, null=True, verbose_name='Превью урока')
    video = models.CharField(max_length=150, blank=True, null=True, verbose_name='Описание урока')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='курс', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

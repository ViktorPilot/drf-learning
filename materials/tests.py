from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonAPITestCase(APITestCase):
    """Класс теста CRUD лекции"""
    def setUp(self):
        """Метод добавления исходных данных для тестирования"""
        self.user = User.objects.create(email='test@ya.ru')
        self.course = Course.objects.create(title='course_1', owner=self.user)
        self.lesson = Lesson.objects.create(title='lesson_1', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user,)

    def test_lesson_retrieve(self):
        """Тестирование вывода данных по лекции"""
        url = reverse("materials:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data= response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonAPITestCase(APITestCase):
    """Класс теста CRUD лекции"""

    def setUp(self):
        """Метод добавления исходных данных для тестирования"""
        self.user = User.objects.create(email="test@ya.ru")
        self.course = Course.objects.create(title="course_1", owner=self.user)
        self.lesson = Lesson.objects.create(title="lesson_1", course=self.course, owner=self.user)
        self.client.force_authenticate(
            user=self.user,
        )

    def test_lesson_retrieve(self):
        """Тестирование вывода данных по лекции"""
        url = reverse("materials:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Тестирование создания лекции"""
        url = reverse("materials:lesson-create")
        data = {"title": "lesson_2", "video": "https://youtube.com/123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тестирование изменения данных по лекции"""
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"title": "lesson_3", "video": "https://youtube.com/456"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "lesson_3")

    def test_lesson_delete(self):
        """Тестирование удаления лекции"""
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тестирование вывода данных по всем лекциям"""
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 4,
                    "video": None,
                    "title": "lesson_1",
                    "description": None,
                    "image": None,
                    "course": 3,
                    "owner": 3,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionAPITestCase(APITestCase):
    """Класс теста подписки"""

    def setUp(self):
        """Метод добавления исходных данных для подписки"""
        self.user = User.objects.create(email="test@ya.ru")
        self.course = Course.objects.create(title="course_2", owner=self.user)
        self.client.force_authenticate(user=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)

    def test_delete_subscriptions(self):
        """Тестирование удаления подписки"""
        url = reverse("materials:subscriptions-create_delete")
        data = {"course_id": self.subscription.course_id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("message"), "подписка удалена")

    def test_create_subscriptions(self):
        """Тестирование создания подписки"""
        url = reverse("materials:subscriptions-create_delete")
        data = {"course_id": self.subscription.course_id}
        self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("message"), "подписка добавлена")

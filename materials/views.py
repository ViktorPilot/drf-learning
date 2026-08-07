from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import MyPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerators, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер API полного CRUD курса"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MyPagination

    def perform_create(self, serializer):
        """Метод добавляет авторизованного пользователя в поле владельца курса"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Метод возвращает отфильтрованные курсы в зависимости от статуса пользователя"""
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        """Метод назначает права доступа к 'actions' в зависимости от роли пользователя"""
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerators]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModerators & IsOwner]
        elif self.action in ["list", "update", "retrieve", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerators | IsOwner]
        return super().get_permissions()


class LessonQuerysetMixin:
    """Миксин для фильтрации лекций в зависимости от статуса пользователя"""

    def get_queryset(self):
        """Метод возвращает отфильтрованные лекции в зависимости от статуса пользователя"""
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonListAPIView(LessonQuerysetMixin, generics.ListAPIView):
    """Контроллер API списка уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerators | IsOwner]
    pagination_class = MyPagination


class LessonUpdateAPIView(LessonQuerysetMixin, generics.UpdateAPIView):
    """Контроллер API редактирования существующего урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerators | IsOwner]


class LessonRetrieveAPIView(LessonQuerysetMixin, generics.RetrieveAPIView):
    """Контроллер API данных урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerators | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер API создания нового урока"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerators]

    def perform_create(self, serializer):
        """Метод добавляет авторизованного пользователя в поле владельца лекции"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonDestroyAPIView(LessonQuerysetMixin, generics.DestroyAPIView):
    """Контроллер API удаления существующего урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerators & IsOwner]


class SubscriptionAPIView(APIView):
    """Контроллер API создания/удаления подписки"""

    def post(self, request, *args, **kwargs):
        """Метод добавления/удаления подписки"""
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message})

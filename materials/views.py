from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerators, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер API полного CRUD курса"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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

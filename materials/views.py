from mypy.dmypy.client import request
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
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerators]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, ~IsModerators & IsOwner]
        elif self.action in ['list', 'update', 'retrieve', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerators | IsOwner]
        return super().get_permissions()


class LessonListAPIView(generics.ListAPIView):
    """Контроллер API списка уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerators | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер API редактирования существующего урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerators | IsOwner]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
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


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер API удаления существующего урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerators & IsOwner]

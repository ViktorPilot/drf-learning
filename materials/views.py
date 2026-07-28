from rest_framework import generics, viewsets

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerators


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер API полного CRUD курса"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [~IsModerators]
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = [IsModerators]
        return super().get_permissions()


class LessonListAPIView(generics.ListAPIView):
    """Контроллер API списка уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер API редактирования существующего урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер API данных урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер API создания нового урока"""

    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер API удаления существующего урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

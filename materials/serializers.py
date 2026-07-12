from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели курса"""

    class Meta:
        """Метакласс сериализатора курса"""

        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели урока"""

    class Meta:
        """Метакласс сериализатора урока"""

        model = Lesson
        fields = "__all__"

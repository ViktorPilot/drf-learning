from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели урока"""

    class Meta:
        """Метакласс сериализатора урока"""

        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели курса"""

    quantity_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_quantity_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        """Метакласс сериализатора курса"""

        model = Course
        fields = "__all__"

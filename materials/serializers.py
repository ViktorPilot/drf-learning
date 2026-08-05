from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import check_not_youtube


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели урока"""
    video = serializers.URLField(validators=[check_not_youtube])

    class Meta:
        """Метакласс сериализатора урока"""

        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели курса"""

    quantity_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    video = serializers.URLField(validators=[check_not_youtube])

    def get_quantity_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        """Метакласс сериализатора курса"""

        model = Course
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели подписки"""

    class Meta:
        """Метакласс сериализатора подписки"""
        model = Subscription
        fields = ['user', 'course']

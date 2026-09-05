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
    is_subscribed = serializers.SerializerMethodField()

    def get_quantity_lessons(self, obj):
        """Метод подсчета количества уроков в курсе"""
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        """Метакласс сериализатора курса"""

        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        """Метод возвращает данные подписан ли текущий пользователь на курс"""
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели подписки"""

    class Meta:
        """Метакласс сериализатора подписки"""

        model = Subscription
        fields = ["user", "course"]

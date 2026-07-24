from rest_framework import serializers

from users.models import Payments, User


class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежа"""

    class Meta:
        """Метакласс сериализатора платежа"""

        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя"""

    payments = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        """Метакласс сериализатора пользователя"""

        model = User
        fields = "__all__"

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """Контроллер API редактирования существующего пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListAPIView(generics.ListAPIView):
    """Контроллер API просмотра списка пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер API просмотра профиля пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateAPIView(generics.CreateAPIView):
    """Контроллер API создания нового пользователя"""

    serializer_class = UserSerializer


class PaymentsListApiView(generics.ListAPIView):
    """Контроллер API просмотра всех платежей"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('date',)
    filterset_fields = ('type_payment', 'bought_course', 'bought_lesson',)

from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """Контроллер API редактирования существующего пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateAPIView(generics.CreateAPIView):
    """Контроллер API создания нового пользователя"""

    serializer_class = UserSerializer

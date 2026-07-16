from django.urls import path

from users import apps
from users.views import UserUpdateAPIView

app_name = apps.UsersConfig.name

urlpatterns = [
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
]

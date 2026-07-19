from django.urls import path

from users import apps
from users.views import PaymentsListApiView, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView

app_name = apps.UsersConfig.name

urlpatterns = [
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("create/", UserCreateAPIView.as_view(), name="user-create"),
    path("", UserListAPIView.as_view(), name="user-list"),
    path("<int:pk>/detail/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("payments/", PaymentsListApiView.as_view(), name="payments-list"),
]

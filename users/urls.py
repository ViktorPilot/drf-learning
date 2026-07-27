from rest_framework.decorators import permission_classes

from users import apps
from users.views import PaymentsListApiView, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny


app_name = apps.UsersConfig.name

urlpatterns = [
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("register/", UserCreateAPIView.as_view(), name="user-register"),
    path("", UserListAPIView.as_view(), name="user-list"),
    path("<int:pk>/detail/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),
    path("payments/", PaymentsListApiView.as_view(), name="payments-list"),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]

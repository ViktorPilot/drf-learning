from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('course/', include('materials.urls', namespace='materials')),
    path('user/', include('users.urls', namespace='users')),
]

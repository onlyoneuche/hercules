from django.contrib import admin
from django.urls import path, include

from users.views import RegisterView, CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/', include('users.urls')),
    path('api/', include('organisations.urls')),
]

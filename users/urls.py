from django.urls import path
from .views import RegisterView, UserDetailView, CustomTokenObtainPairView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', CustomTokenObtainPairView.as_view(), name='login'),
    path('users/<str:userId>', UserDetailView.as_view(), name='user-detail'),
]


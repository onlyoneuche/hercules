from django.urls import path
from .views import UserDetailView

urlpatterns = [
    path('users/<str:userId>', UserDetailView.as_view(), name='user-detail'),
]


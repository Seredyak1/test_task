from django.urls import path

from user_profile.views import RegistrationsAPIView, UserDetailAPIView

urlpatterns = [
    path('', RegistrationsAPIView.as_view()),
    path('<int:pk>/', UserDetailAPIView.as_view()),
]

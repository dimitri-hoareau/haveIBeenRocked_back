from django.urls import path
from .views import PasswordCheckView

urlpatterns = [
    path('api/check-password/', PasswordCheckView.as_view(), name='check_password'),
]
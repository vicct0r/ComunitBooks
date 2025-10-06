from django.urls import path
from .views import UserSignupView

app_name = 'user'

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name='signup')
]
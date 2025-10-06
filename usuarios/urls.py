from django.urls import path
from .views import UserSignupView

app_name = 'usuario'

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name='user_signup')
]
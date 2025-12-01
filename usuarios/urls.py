from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path("signup/", views.UserSignupView.as_view(), name='signup'),
    path('profile/<uuid:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<uuid:user_id>/update/', views.UserUpdateView.as_view(), name='profile_update')
]
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.conf import settings
from django.urls import reverse_lazy

from .models import CustomUser
from .forms import CustomUserCreationForm


class UserSignupView(generic.CreateView):
    template_name = 'usuarios/signup.html'
    form_class = CustomUserCreationForm
    model = settings.AUTH_USER_MODEL
    success_url = reverse_lazy('core:home')

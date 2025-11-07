from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomUserChangeForm


class UserSignupView(generic.CreateView):
    template_name = 'usuarios/signup.html'
    form_class = CustomUserCreationForm
    model = get_user_model()
    success_url = reverse_lazy('core:home')


class UserProfileView(generic.DetailView):
    template_name = 'usuarios/my_profile.html'
    model = get_user_model()
    context_object_name = 'user'
    lookup_field = 'id'

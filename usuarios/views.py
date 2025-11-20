from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomUserChangeForm


class UserSignupView(generic.CreateView):
    template_name = 'usuarios/signup.html'
    form_class = CustomUserCreationForm
    model = get_user_model()
    success_url = reverse_lazy('core:home')


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = 'usuarios/my_profile.html'
    model = get_user_model()
    context_object_name = 'user'
    lookup_field = 'id'


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'usuarios/change_user_info.html'
    model = get_user_model()
    form_class = CustomUserChangeForm
    lookup_field = 'id'

    def get_success_url(self):
        return reverse('user:profile', kwargs={'pk': self.request.user.id})

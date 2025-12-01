from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomUserChangeForm
from . import services


class UserSignupView(generic.CreateView):
    template_name = 'usuarios/signup.html'
    form_class = CustomUserCreationForm
    model = get_user_model()
    success_url = reverse_lazy('core:home')


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = 'usuarios/my_profile.html'
    model = get_user_model()
    context_object_name = 'user'
    lookup_field = 'user_id'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['orders_received'] = services.orders_received(user)
        context['loans_received'] = services.loans_received(user)
        context['orders_submitted'] = services.orders_submitted(user)
        context['loans_submitted'] = services.loans_submitted(user)
        return context
    

class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'usuarios/change_user_info.html'
    model = get_user_model()
    form_class = CustomUserChangeForm
    lookup_field = 'user_id'

    def get_success_url(self):
        return reverse('user:profile', kwargs={'pk': self.request.user.id})

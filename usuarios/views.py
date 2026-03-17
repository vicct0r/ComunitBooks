from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
import requests

from .models import Address
from .forms import CustomUserCreationForm, CustomUserChangeForm, AddressForm
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
    pk_url_kwarg = 'user_id'

    def get_queryset(self):
        return super().get_queryset().select_related('address')

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
    pk_url_kwarg = 'user_id'

    def get_success_url(self):
        return reverse('user:profile', kwargs={'user_id': self.request.user.id})


class AttachAddressView(LoginRequiredMixin, generic.View):
    template_name = 'usuarios/address_form.html'

    def get(self, request, *args, **kwargs):
        form = AddressForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        address = form.save()
        request.user.address = address
        request.user.save(update_fields=['address'])
        return redirect('user:profile', user_id=request.user.id)

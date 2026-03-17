from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Address


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name']
        labels = {'email': 'Email'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'img', 'phone']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['cep', 'logradouro', 'complemento', 'bairro', 'localidade', 'estado', 'regiao']
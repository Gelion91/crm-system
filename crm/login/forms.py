from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.forms import ModelForm


class RegistrationForm(ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'autocomplete': 'new-password'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    groups = forms.CheckboxSelectMultiple(choices=Group.objects.all())

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'groups']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password']


class UpdateUserForm(ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'autocomplete': 'new-password'}))
    groups = forms.CheckboxSelectMultiple(choices=Group.objects.all())

    class Meta:
        model = User
        fields = ['username','groups']

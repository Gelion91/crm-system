from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from core.forms import CustomAuthForm


class LoginUser(LoginView):
    form_class = CustomAuthForm
    template_name = 'login/login.html'

    redirect_authenticated_user = 'core:home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        if self.request.user.groups.filter(name='managers'):
            print('True')
            return reverse_lazy('core:home')
        elif self.request.user.groups.filter(name='logist'):
            return reverse_lazy('core:status_product')
        else:
            return reverse_lazy('core:home')


def logout_view(request):
    logout(request)
    return redirect('login:login')

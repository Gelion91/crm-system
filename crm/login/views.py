from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from core.forms import CustomAuthForm
from login.forms import RegistrationForm, UpdateUserForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            for gp in form.cleaned_data['groups']:
                group = Group.objects.get(pk=gp.pk)
                user.groups.add(group)
            return render(request, 'login/register_done.html')
    else:
        form = RegistrationForm()
    return render(request, 'login/register.html', {'form': form})


def change_user_info(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            print('Успех')
            user = form.save(commit=False)
            user.save()
            user.groups.clear()
            for gp in form.cleaned_data['groups']:
                group = Group.objects.get(pk=gp.pk)
                user.groups.add(group)
            return render(request, 'login/update_user_done.html')
        print(form.errors)
        print('Успех')
    else:
        print('Успех')
        form = UpdateUserForm(instance=user)
    return render(request, 'login/update_user.html', {'form': form})


# def change_user_info(request, user_id):
#     user = User.objects.get(pk=user_id)
#     if request.method == 'POST':
#         form = UpdateUserForm(request.POST, instance=user)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             user.groups.clear()
#             for gp in form.cleaned_data['groups']:
#                 group = Group.objects.get(pk=gp.pk)
#                 user.groups.add(group)
#             return render(request, 'login/update_user.html')
#     else:
#         form = UpdateUserForm(instance=user)
#     return render(request, 'login/update_user.html', {'form': form})


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

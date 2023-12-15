from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView

from clients.filters import ClientFilter
from clients.forms import AddClientForm
from core.models import Clients


class ClientsListView(LoginRequiredMixin, FilterView):
    model = Clients
    paginate_by = 16
    template_name = 'clients/clients_list.html'
    filterset_class = ClientFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClientFilter.form
        context['title'] = 'Список клиентов'
        print(context)
        return context


class ActiveClientsListView(ClientsListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClientFilter.form
        context['title'] = 'Мои клиенты'
        print(context)
        return context

    def get_queryset(self):
        return Clients.objects.filter(result=True)


class MyClientsListView(ClientsListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClientFilter.form
        context['title'] = 'Мои клиенты'
        print(context)
        return context

    def get_queryset(self):
        return Clients.objects.filter(owner=self.request.user)


class AddClient(LoginRequiredMixin, CreateView):
    form_class = AddClientForm
    template_name = 'clients/addclient.html'
    success_url = reverse_lazy('clients:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить клиента'
        return context


class UpdateClient(UpdateView):
    model = Clients
    form_class = AddClientForm
    pk_url_kwarg = 'client_id'
    template_name = 'clients/updateclient.html'

    def get_success_url(self):
        return reverse('clients:home')

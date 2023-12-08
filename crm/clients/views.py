from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django_filters.views import FilterView

from clients.filters import ClientFilter
from core.models import Clients


class ClientsListView(LoginRequiredMixin, FilterView):
    model = Clients
    paginate_by = 16
    template_name = 'clients/clients_list.html'
    filterset_class = ClientFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClientFilter.form
        context['title'] = 'Список заказов'
        print(context)
        return context

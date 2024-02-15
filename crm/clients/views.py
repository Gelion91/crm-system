from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from clients.filters import ClientFilter
from clients.forms import AddClientForm, CommentForm
from clients.models import Comments
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
        return context


class ActiveClientsListView(ClientsListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClientFilter.form
        context['title'] = 'Мои клиенты'
        return context

    def get_queryset(self):
        return Clients.objects.filter(result=True)


class MyClientsListView(ClientsListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClientFilter.form
        context['title'] = 'Мои клиенты'
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


class ClientDetail(FormMixin, DetailView):
    template_name = 'clients/detailclient.html'
    model = Clients
    pk_url_kwarg = 'client_id'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('clients:detail_client', kwargs={'client_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ClientDetail, self).get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(client=self.object).order_by('date_create')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.client = self.object
        form.save()
        return super(ClientDetail, self).form_valid(form)


def delete_comment(request, pk):
    comment = Comments.objects.get(pk=pk)
    client = comment.client.pk
    comment.delete()
    return redirect('clients:detail_client', client)
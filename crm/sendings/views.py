import json

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import dateformat
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.views.generic.edit import FormMixin

from core.models import Logistics
from crm import settings
from sendings.filters import SendingFilter
from sendings.forms import SendingCreateForm, CarrierAddForm, SendingNotesForm, SimplySendingForm
from sendings.models import Sending, Carriers, NotesSending


class SendingsStatus(LoginRequiredMixin, FilterView):
    model = Sending
    paginate_by = 16
    template_name = 'sendings/sendings_list.html'

    filterset_class = SendingFilter
    # form_class = LogisticImageForm

    def get_queryset(self):
        return Sending.objects.filter(second_step=False)

    def get_success_url(self):
        return reverse('sendings:status_sending')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SendingFilter.form
        context['notes_form'] = SendingNotesForm
        context['title'] = 'Отправки'
        context['groups'] = self.request.user.groups.filter(name='logist').exists()
        context['china'] = self.request.user.groups.filter(name='china').exists()
        return context


def change_sending_status(request):
    sending_id = request.POST.get("id")
    sending = Sending.objects.get(pk=sending_id)
    checked = request.POST.get("checked")
    attribut = request.POST.get("attribut").split('-')[0]
    if checked == 'true':
        result = True
    else:
        result = False
    if attribut == 'first_step':
        sending.first_step = result
    elif attribut == 'second_step':
        sending.second_step = result
    sending.save()

    response = {
        'OK': 200
    }
    return JsonResponse(response)


def change_sending(request):
    sending_id = request.POST.get("id").split('_')[-1]
    marker = request.POST.get("marker")
    weight = request.POST.get("weight")
    volume = request.POST.get("volume")
    places = request.POST.get("places")
    sending = Sending.objects.get(pk=sending_id)
    sending.marker, sending.weight, sending.volume = marker, weight, volume
    sending.save()
    response = {
        'marker': marker,
        'sending_id': sending_id,
    }
    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')


def save_notes_sending(request):
    note = request.POST.get("note")
    sending_id = request.POST.get("id")
    comment = NotesSending(sending=Sending.objects.get(pk=sending_id), comment=note, owner=request.user)
    comment.save()
    print(comment.date_create)
    response = {
        'note': note,
        'sending': sending_id,
        'comment_id': comment.pk,
        'user': request.user.username,
        'date': dateformat.format(comment.date_create, settings.DATE_FORMAT).lstrip('0'),
    }
    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')


def delete_notes_sending(request):
    notes_id = request.POST.get("id").split('_')[-1]
    print(notes_id)
    comment = NotesSending.objects.get(pk=notes_id)
    comment.delete()
    response = {
        'notes_id': notes_id,
    }
    print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')


class SendingCreate(LoginRequiredMixin, CreateView):
    model = Sending
    form_class = SendingCreateForm
    template_name = 'sendings/sending_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформить отправку'
        context['carrier_form'] = CarrierAddForm()
        return context

    def get_success_url(self):
        return reverse('sendings:sendings_list')

    def get_form_kwargs(self):
        kwargs = super(SendingCreate, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def create_carrier(request):
    carrier_name = request.POST.get("name")
    carrier_comment = request.POST.get("comment")
    print(carrier_name)
    print(carrier_comment)
    carrier = Carriers(name=carrier_name, comment=carrier_comment)
    carrier.save()
    print(carrier)

    response = {
        'carrier_name': carrier.name,
        'carrier_comment': carrier_comment,
        'carrier_id': carrier.pk
    }

    # response = {'ok':200}
    return HttpResponse(json.dumps(response), content_type='application/json')


def get_info(request):
    logistic_id = request.POST.get("id")
    logistic = Logistics.objects.get(pk=logistic_id)
    response = {
        'price': logistic.order_price,
        'weight': logistic.weight,
        'volume': logistic.volume,
        'places': logistic.places
    }

    return JsonResponse(response)


def show_logistic_info(request):
    logistic_id = request.POST.get("id")
    logistic = Logistics.objects.get(pk=logistic_id)

    response = {
        'marker': logistic.marker,
        'delivery_price': float(logistic.tariff),
        'products_price': float(logistic.order_price),
        'owner': logistic.owner.username if logistic.owner else None,
        'weight': float(logistic.weight),
        'volume': float(logistic.volume),
        'density': float(logistic.density),
        'insurance': float(logistic.insurance),
        'user': request.user.username if request.user else None,
    }

    return HttpResponse(json.dumps(response), content_type='application/json')


class SendingUpdate(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingCreateForm
    pk_url_kwarg = 'sending_id'
    template_name = 'sendings/sending_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить отправку'
        context['carrier_form'] = CarrierAddForm()
        return context

    def get_success_url(self):
        return reverse('sendings:sendings_list')

    def get_form_kwargs(self):
        kwargs = super(SendingUpdate, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


class SendingDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Sending
    permission_required = 'sendings.delete_sending'
    context_object_name = 'sending'
    pk_url_kwarg = "sending_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

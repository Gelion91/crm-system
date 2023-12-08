import django_filters
from django import forms
from django_filters import DateFromToRangeFilter, MultipleChoiceFilter, AllValuesMultipleFilter
from django_filters.widgets import RangeWidget, DateRangeWidget

from core.models import Clients


class DatInput(forms.DateInput):
    input_type = 'date'


class ClientFilter(django_filters.FilterSet):
    date_create = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'class': "form-control", 'type': 'date'}))

    class Meta:
        model = Clients
        fields = ['name', 'owner', 'result', 'date_create']

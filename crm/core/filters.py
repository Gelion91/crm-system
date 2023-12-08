import django_filters
from django import forms
from django_filters import DateFromToRangeFilter, MultipleChoiceFilter, AllValuesMultipleFilter
from django_filters.widgets import RangeWidget, DateRangeWidget

from core.models import Order


class DatInput(forms.DateInput):
    input_type = 'date'


class OrderFilter(django_filters.FilterSet):
    date_create = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'class': "form-control", 'type': 'date'}))

    class Meta:
        model = Order
        fields = ['client', 'status', 'date_create']

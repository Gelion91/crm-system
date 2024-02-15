import django_filters
from django import forms
from django.contrib.auth.models import User
from django_filters import DateFromToRangeFilter, MultipleChoiceFilter, AllValuesMultipleFilter
from django_filters.widgets import RangeWidget, DateRangeWidget

from core.models import Order


class DatInput(forms.DateInput):
    input_type = 'date'


class OrderChartFilter(django_filters.FilterSet):
    CHOICES = (
        ('ascending', 'Cначала новые'),
        ('descending', 'Сначала старые')
    )
    date_create = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'class': "form-control", 'type': 'date'}))
    ordering = django_filters.ChoiceFilter(label='Сортировать', choices=CHOICES, method='filter_by_order')


    class Meta:
        model = Order
        fields = ['date_create', 'owner', 'status']

    def filter_by_order(self, queryset, name, value):
        expression = '-date_create' if value == 'ascending' else 'date_create'
        return queryset.order_by(expression)

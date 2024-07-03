import django_filters
from django import forms
from django_filters import DateFromToRangeFilter, MultipleChoiceFilter, AllValuesMultipleFilter
from django_filters.widgets import RangeWidget, DateRangeWidget

from core.models import Order, Product, Logistics
from sendings.models import Sending


class DatInput(forms.DateInput):
    input_type = 'date'


class SendingFilter(django_filters.FilterSet):
    CHOICES_ORDER = (
        ('marker', 'По маркировке'),
        ('-marker', 'По маркировке в обратном порядке'),
        ('owner', 'По менеджерам'),
        ('-owner', 'По менеджерам в обратном порядке')
    )
    date_create = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'class': "form-control", 'type': 'date'}))

    CHOICES = (
        ('all', 'Все'),
        ('in_work', 'Текущие'),
    )

    DELIVERY_CHOICES = [
        ('auto', "Авто"),
        ('auto_express', "Авто-экспресс"),
        ('rail', "Жд"),
        ('avia', "Авиа"),
    ]
    ordering = django_filters.ChoiceFilter(label='Сортировать', choices=CHOICES_ORDER, method='filter_by_order')
    marker = django_filters.CharFilter(label='Поиск по маркировке', method='filter_by_marker')
    status = django_filters.ChoiceFilter(label='Статус', choices=CHOICES, method='filter_by_status')
    type_arrive = django_filters.ChoiceFilter(label='Тип отправления', choices=DELIVERY_CHOICES,
                                              method='filter_by_type')
    date_create = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'class': "form-control", 'type': 'date'}))

    @property
    def qs(self):
        queryset = super().qs
        if self.request.user.is_superuser or self.request.user.groups.filter(name='logist').exists() or self.request.user.groups.filter(name='china').exists():
            return queryset
        else:
            return queryset.filter(product__owner=self.request.user.pk).distinct()

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)

    def filter_by_status(self, queryset, name, value):
        if value == 'all':
            queryset1 = Sending.objects.all()
            queryset = (queryset | queryset1)
        return queryset

    def filter_by_marker(self, queryset, name, value):
        return queryset.filter(marker__icontains=value)

    def filter_by_type(self, queryset, name, value):
        if value:
            choices = self.DELIVERY_CHOICES
            for choice in choices:
                if value in choice:
                    queryset = queryset.filter(delivery=choice[-1])
            return queryset
        else:
            queryset = queryset
            return queryset


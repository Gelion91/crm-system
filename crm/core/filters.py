import django_filters
from django import forms
from django_filters import DateFromToRangeFilter, MultipleChoiceFilter, AllValuesMultipleFilter
from django_filters.widgets import RangeWidget, DateRangeWidget

from core.models import Order, Product, Logistics


class DatInput(forms.DateInput):
    input_type = 'date'


class OrderFilter(django_filters.FilterSet):
    CHOICES = (
        ('ascending', 'Cначала новые'),
        ('descending', 'Сначала старые')
    )
    date_create = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'class': "form-control", 'type': 'date'}))

    ordering = django_filters.ChoiceFilter(label='Сортировать', choices=CHOICES, method='filter_by_order')

    def filter_by_order(self, queryset, name, value):
        expression = '-date_create' if value == 'ascending' else 'date_create'
        return queryset.order_by(expression)

    class Meta:
        model = Order
        fields = ['client', 'status', 'date_create']


class ProductFilter(django_filters.FilterSet):
    CHOICES = (
        ('all', 'Все'),
        ('arrived', 'Отправленные'),
        ('waited', 'Ожидают отправки')
    )

    marker = django_filters.CharFilter(label='Поиск по маркировке', method='filter_by_marker')
    logist = django_filters.ChoiceFilter(label='Показать', choices=CHOICES, method='filter_by_status')

    def filter_by_marker(self, queryset, name, value):
        return queryset.filter(product_marker__icontains=value)

    def filter_by_status(self, queryset, name, value):
        if value == 'all':
            queryset = Product.objects.all()
            return queryset
        elif value == 'arrived':
            queryset = Product.objects.filter(logistics__isnull=False)
            return queryset
        else:
            queryset = Product.objects.filter(logistics=None)
            return queryset

    class Meta:
        model = Product
        fields = ['paid', 'arrive']


class DeliveryFilter(django_filters.FilterSet):
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
    marker = django_filters.CharFilter(label='Поиск по маркировке', method='filter_by_marker')
    status = django_filters.ChoiceFilter(label='Статус', choices=CHOICES, method='filter_by_status')
    type_arrive = django_filters.ChoiceFilter(label='Тип отправления', choices=DELIVERY_CHOICES,
                                              method='filter_by_type')
    date_create = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'class': "form-control", 'type': 'date'}))

    @property
    def qs(self):
        parent = super().qs
        owner = self.request.user
        if self.request.user.is_superuser or self.request.user.groups.filter(name='logist').exists():
            return parent
        else:
            return parent.filter(owner=owner)

    def filter_by_marker(self, queryset, name, value):
        return Logistics.objects.filter(marker__icontains=value)

    def filter_by_status(self, queryset, name, value):
        if value == 'all':
            queryset = Logistics.objects.all()
        return queryset

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


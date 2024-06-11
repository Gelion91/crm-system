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

    CHOICES_ORDER = (
        ('product_marker', 'По маркировке'),
        ('-product_marker', 'По маркировке в обратном порядке'),
        ('owner', 'По менеджерам'),
        ('-owner', 'По менеджерам в обратном порядке')
    )

    ordering = django_filters.ChoiceFilter(label='Сортировать', choices=CHOICES_ORDER, method='filter_by_order')
    marker = django_filters.CharFilter(label='Поиск по маркировке', method='filter_by_marker')
    logist = django_filters.ChoiceFilter(label='Показать', choices=CHOICES, method='filter_by_status')

    @property
    def qs(self):
        parent = super().qs
        owner = self.request.user
        if self.request.user.is_superuser or self.request.user.groups.filter(name='logist').exists():
            return parent
        else:
            return parent.filter(owner=owner)

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)

    def filter_by_marker(self, queryset, name, value):
        # if self.request.user.is_superuser or self.request.user.groups.filter(name='logist').exists():
        #     queryset = Product.objects.all()
        # else:
        #     queryset = Product.objects.filter(owner=self.request.user)
        return queryset.filter(product_marker__icontains=value)

    def filter_by_status(self, queryset, name, value):
        if value == 'all':
            queryset1 = Product.objects.all()
            queryset = (queryset | queryset1)
            return queryset
        elif value == 'arrived':
            queryset1 = Product.objects.all()
            queryset = (queryset | queryset1)
            return queryset.filter(logistics__isnull=False)
        else:
            return queryset.filter(logistics=None)

    class Meta:
        model = Product
        fields = ['paid', 'arrive']


class DeliveryFilter(django_filters.FilterSet):
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
        parent = super().qs
        owner = self.request.user
        if self.request.user.is_superuser or self.request.user.groups.filter(name='logist').exists():
            return parent
        else:
            return parent.filter(owner=owner)

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)

    def filter_by_status(self, queryset, name, value):
        if value == 'all':
            queryset1 = Logistics.objects.all()
            queryset = (queryset | queryset1)
        return queryset

    def filter_by_marker(self, queryset, name, value):
        # if self.request.user.is_superuser or self.request.user.groups.filter(name='logist').exists():
        #     queryset = Logistics.objects.all()
        # else:
        #     queryset = Logistics.objects.filter(owner=self.request.user)
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


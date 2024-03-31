from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.shortcuts import render

from core.models import Order
from dashboard.filters import OrderChartFilter
""".values(day=TruncDay('date_create')).annotate(Count('id'), Sum('total_price_rub'))"""


def chart(request):
    filter = OrderChartFilter(request.GET, queryset=Order.objects.all())
    context = {'users': [
        {
            'id': obj.id,
            'username': obj.username,
            'summa': sum([i.total_price_rub for i in filter.qs.filter(owner=obj) if i.status == "Завершен"])
        }
        for obj in User.objects.all()],
        'filter': filter,
        'complete': filter.qs.filter(status='Завершен').count(),
        'inwork': filter.qs.filter(status='Оформление').count(),
        'onpay': filter.qs.filter(status='На оплату').count(),
        'dataset_complete': filter.qs.filter(status='Завершен').values(day=TruncDay('date_create')).annotate(Count('id'), Sum('total_price_rub')),
        'dataset_all': filter.qs.values(day=TruncDay('date_create')).annotate(Count('id'), Sum('total_price_rub')),
        'total_sum': filter.qs.aggregate(Sum('total_price_rub'))
    }
    return render(request, 'dashboard/charts.html', context)


# class OrderChartView(FilterView):
#     model = Order
#     template_name = 'dashboard/order_chart.html'
#     filterset_class = OrderChartFilter
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Список заказов'
#
#         context['users'] = [
#             {
#                 'id': obj.id,
#                 'username': obj.username,
#                 'summa': sum([i.total_price_rub for i in obj.order_set.all() if i.status == "Завершен"])
#             }
#             for obj in User.objects.all()
#         ]
#
#         context['form'] = OrderChartFilter.form
#         # print([i.order_set.all() for i in context['users']])
#         return context

from django.contrib.auth.decorators import login_required

from core.models import Order, Clients


def menu_manager(request):
    menu = [{'title': 'клиенты', 'url_name': 'clients:home', 'submenu': [{'title': 'Добавить клиента', 'url_name': 'clients:addclient'},
                                                                         {'title': 'Активные клиенты', 'url_name': 'clients:active'},
                                                                         {'title': 'Мои клиенты', 'url_name': 'clients:my_clients'},
                                                                         {'title': 'Надо позвонить', 'url_name': 'clients:home'}]},

            {'title': 'Заказы', 'url_name': 'core:home', 'submenu': [{'title': 'Оформить заказ', 'url_name': 'core:addorder'},
                                                                     {'title': 'Активные заказы', 'url_name': 'core:active'},
                                                                     {'title': 'Ожидают оплаты', 'url_name': 'core:on_pay'},
                                                                     {'title': 'Завершенные заказы', 'url_name': 'core:finish'}]},

            {'title': 'Доставка', 'url_name': 'core:logistic', 'submenu': [{'title': 'Оформить доставку', 'url_name': 'core:add_delivery'},
                                                                           ]},

            {'title': 'Панель управления', 'url_name': 'dashboard:home', 'submenu': [{'title': 'Общее', 'url_name': 'dashboard:home'},
                                                                     ]}
            ]

    return {'menu': menu}


def get_complete_orders(request):
    if request.user.is_authenticated:
        return {'success_orders': Order.objects.filter(owner=request.user).filter(status='Завершен').count(),
                'my_orders': Order.objects.filter(owner=request.user).count()}
    else:
        return {'success_orders': Order.objects.none(),
                'my_orders': Order.objects.none()}


def get_clients_info(request):
    if request.user.is_authenticated:
        return {'clients': Clients.objects.all().count(),
                'my_clients': Clients.objects.filter(owner=request.user).count(),
                'success_client': Clients.objects.filter(owner=request.user).filter(result=True).count()}

    else:
        return {'clients': Clients.objects.none(),
                'my_clients': Clients.objects.none(),
                'success_client': Clients.objects.none()}

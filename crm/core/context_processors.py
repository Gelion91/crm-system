from django.contrib.auth.decorators import login_required

from core.models import Order, Clients


def menu_manager(request):
    menu = [{'title': 'клиенты', 'url_name': 'clients:home'},
            {'title': 'Заказы', 'url_name': 'core:home'},
            {'title': 'Добавить клиента', 'url_name': 'core:addclient'},
            {'title': 'Оформить заказ', 'url_name': 'core:addorder'}
            ]
    if request.user.groups.filter(id=1):
        menu = [{'title': 'Список клиентов', 'url_name': 'clients:home'},
                {'title': 'Добавить клиента', 'url_name': 'core:addclient'},
                ]

    elif request.user.groups.filter(id=2):
        menu = [{'title': 'Список заказов', 'url_name': 'core:home'},
                {'title': 'Оформить заказ', 'url_name': 'core:addorder'}
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

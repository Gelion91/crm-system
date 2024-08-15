from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry
from django.db.models import Q

from core.models import Order, Clients, Course, Notification

'''{'title': 'Панель управления', 'url_name': 'dashboard:home',
             'submenu': [{'title': 'Общее', 'url_name': 'dashboard:home'},
                         ]},'''


def menu_manager(request):
    if not request.user.is_authenticated:
        menu = {}
        return {'menu': menu}

    if request.user.is_superuser:
        menu = [{'title': 'клиенты', 'url_name': 'clients:home',
                 'submenu': [
                     {'title': 'Добавить клиента', 'url_name': 'clients:addclient', 'path': 'clients/addclient/'},
                     {'title': 'Активные клиенты', 'url_name': 'clients:active', 'path': 'clients/active_clients'},
                     {'title': 'Мои клиенты', 'url_name': 'clients:my_clients', 'path': 'clients/my_clients'}]},

                {'title': 'Заказы', 'url_name': 'core:home',
                 'submenu': [{'title': 'Оформить заказ', 'url_name': 'core:addorder', 'path': 'orders/addorder/'},
                             {'title': 'Все заказы', 'url_name': 'core:all', 'path': 'orders/all/'},
                             {'title': 'Ожидают отправки', 'url_name': 'core:on_pay', 'path': 'orders/on_pay/'},
                             {'title': 'Завершенные заказы', 'url_name': 'core:finish', 'path': 'orders/finish/'}]},

                {'title': 'Доставка', 'url_name': 'core:status_delivery',
                 'submenu': [
                     {'title': 'Оформить доставку', 'url_name': 'core:add_delivery', 'path': 'logistic/add_delivery'},
                     {'title': 'Статус товаров', 'url_name': 'core:status_product', 'path': 'logistic/sp'},
                     {'title': 'Завершенные доставки', 'url_name': 'core:archive', 'path': 'logistic/archive'},
                     ]},
                {'title': 'Отправки', 'url_name': 'sendings:sendings_list',
                 'submenu': [
                     {'title': 'Оформить отправку', 'url_name': 'sendings:sending_create', 'path': '/sending_create'},
                 ]},
                {'title': 'Управление аккаунтами', 'url_name': 'core:add_account'},
                {'title': 'Финансы', 'url_name': 'core:finance_list', 'submenu': [
                     {'title': 'Добавить трату', 'url_name': 'core:add_spending', 'path': 'finance/add_spending'},
                     {'title': 'Список затрат', 'url_name': 'core:list_spendings', 'path': 'finance/spendings/'},
                 ]},
                ]
        return {'menu': menu}

    elif request.user.groups.filter(name='managers'):
        menu = [{'title': 'клиенты', 'url_name': 'clients:home',
                 'submenu': [{'title': 'Добавить клиента', 'url_name': 'clients:addclient', 'path': 'clients/addclient/'},
                             {'title': 'Активные клиенты', 'url_name': 'clients:active', 'path': 'clients/active_clients'},
                             {'title': 'Мои клиенты', 'url_name': 'clients:my_clients', 'path': 'clients/my_clients'}]},

                {'title': 'Заказы', 'url_name': 'core:home',
                 'submenu': [{'title': 'Оформить заказ', 'url_name': 'core:addorder', 'path': 'orders/addorder/'},
                             {'title': 'Все заказы', 'url_name': 'core:all', 'path': 'orders/all/'},
                             {'title': 'Ожидают отправки', 'url_name': 'core:on_pay', 'path': 'orders/on_pay/'},
                             {'title': 'Завершенные заказы', 'url_name': 'core:finish', 'path': 'orders/finish/'}]},

                {'title': 'Доставка', 'url_name': 'core:status_delivery',
                 'submenu': [{'title': 'Оформить доставку', 'url_name': 'core:add_delivery', 'path': 'logistic/add_delivery'},
                             {'title': 'Статус товаров', 'url_name': 'core:status_product', 'path': 'logistic/sp'},
                             {'title': 'Завершенные доставки', 'url_name': 'core:archive', 'path': 'logistic/archive'},
                             ]}
                ]
        return {'menu': menu}

    elif request.user.groups.filter(name='logist'):
        menu = [{'title': 'клиенты', 'url_name': 'clients:home',
                 'submenu': [
                     {'title': 'Добавить клиента', 'url_name': 'clients:addclient', 'path': 'clients/addclient/'},
                     {'title': 'Активные клиенты', 'url_name': 'clients:active', 'path': 'clients/active_clients'},
                     {'title': 'Мои клиенты', 'url_name': 'clients:my_clients', 'path': 'clients/my_clients'}]},

                {'title': 'Доставка', 'url_name': 'core:status_delivery',
                 'submenu': [
                     {'title': 'Оформить доставку', 'url_name': 'core:add_delivery', 'path': 'logistic/add_delivery'},
                     {'title': 'Статус товаров', 'url_name': 'core:status_product', 'path': 'logistic/sp'},
                     {'title': 'Завершенные доставки', 'url_name': 'core:archive', 'path': 'logistic/archive'},
                     ]},
                {'title': 'Отправки', 'url_name': 'sendings:sendings_list',
                 'submenu': [
                     {'title': 'Оформить отправку', 'url_name': 'sendings:sending_create', 'path': '/sending_create'},
                 ]}
                ]
        return {'menu': menu}

    elif request.user.groups.filter(name='china'):
        menu = [{'title': 'Доставка', 'url_name': 'core:status_delivery',
                 'submenu': [
                     {'title': 'Статус товаров', 'url_name': 'core:status_product', 'path': 'logistic/sp'},
                     {'title': 'Завершенные доставки', 'url_name': 'core:archive', 'path': 'logistic/archive'},
                     ]},
                {'title': 'Отправки', 'url_name': 'sendings:sendings_list',
                 'submenu': [
                     {'title': 'Оформить отправку', 'url_name': 'sendings:sending_create', 'path': '/sending_create'},
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


def course_today(request):
    crs = Course.objects.last()
    if crs:
        return {'dollar_course': crs.course,
                'date_review_course': crs.date_create}
    else:
        return {'dollar_course': 'Еще нету данных',
                'date_review_course': 'Еще нету данных'}


def notification_count(request):
    if request.user.is_authenticated:
        notification = Notification.objects.filter(readed=False, subject_owner=request.user).filter(
                                                ~Q(notifications__readers__in=[request.user.pk])).count()
        return {'notifications': notification}
    else:
        return {'notifications': Notification.objects.none()}
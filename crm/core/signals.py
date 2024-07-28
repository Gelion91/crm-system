import json
import os

import channels
import django.dispatch
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict

from core.models import Order, Clients, Product, Logistics, Notification


@receiver(pre_save, sender=Logistics)
def create_logistic(sender, instance, **kwargs):
    act = 'Создал'
    if instance.pk:
        old_logistic = Logistics.objects.get(pk=instance.pk)
        if old_logistic.first_step != instance.first_step:
            act = f'Статус изменен на {"Отправлен" if instance.first_step else "Еще не отправлен"}'
        elif old_logistic.second_step != instance.second_step:
            act = f'Статус изменен на {"Пришел в Москву" if instance.second_step else "Отправлен"}'
        elif old_logistic.third_step != instance.third_step:
            act = f'Статус изменен на {"Прибыл клиенту" if instance.third_step else "Пришел в Москву"}'

    notification = Notification(owner=instance.last_updater, subject=f'доставку {instance.marker}', action=act,
                                subject_owner=instance.owner)
    notification.save()

    request_args = {
        'last_updater': instance.last_updater.username if instance.last_updater else 'Безымянный',
        'subject': f'Груз {instance.marker}',
        'action': act,
        'owner': instance.owner.username,
        'notification_count': Notification.objects.filter(readed=False, subject_owner=instance.owner).count()
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "echo_group",
        {"type": "stream", "data": request_args},
    )


@receiver(post_save, sender=Logistics)
def change_logistic(sender, instance, created, **kwargs):
    if not created:
        if instance.sendings.all():
            sending = instance.sendings.first()
            sending.weight = sum(i.weight for i in sending.logistics.all())
            sending.volume = sum(i.volume for i in sending.logistics.all())
            sending.places = sum(i.places for i in sending.logistics.all())
            sending.save()


@receiver(post_delete, sender=Logistics)
def delete_logistic(sender, instance, **kwargs):
    act = 'удалил'
    notification = Notification(owner=instance.owner, subject=f'доставку {instance.marker}', action=act)
    notification.save()


@receiver(pre_save, sender=Product)
def create_product(sender, instance, **kwargs):
    act = 'Создал'
    if instance.pk:
        old_product = Product.objects.get(pk=instance.pk)
        if old_product.arrive != instance.arrive:
            act = f'Статус изменен на {"Прибыл" if instance.arrive else "Еще не пришел"}'

    notification = Notification(owner=instance.last_updater,
                                subject=f'продукт {instance.product_marker}({instance.name})',
                                action=act, subject_owner=instance.owner)
    notification.save()

    request_args = {
        'last_updater': instance.last_updater.username if instance.last_updater else 'Безымянный',
        'subject': f'товар {instance.product_marker}',
        'action': act,
        'owner': instance.owner.username,
        'notification_count': Notification.objects.filter(readed=False, subject_owner=instance.owner).count()
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "echo_group",
        {"type": "stream", "data": request_args},
    )


@receiver(post_delete, sender=Product)
def create_product(sender, instance, **kwargs):
    act = 'удалил'
    notification = Notification(owner=instance.owner, subject=f'продукт {instance.product_marker}({instance.name})',
                                action=act, subject_owner=instance.owner)
    notification.save()


@receiver(post_save, sender=Order)
def create_product(sender, instance, created, **kwargs):
    if created:
        act = 'Создал(а) заказ'
        notification = Notification(owner=instance.owner, subject=f'заказ {instance.marker}', action=act,
                                    subject_owner=instance.owner)
        notification.save()

        request_args = {
            'last_updater': instance.owner.username,
            'subject': instance.marker,
            'action': act,
            'notification_count': Notification.objects.filter(readed=False, subject_owner=instance.owner).count()
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "echo_group",
            {"type": "new_order", "data": request_args},
        )


@receiver(post_delete, sender=Order)
def create_product(sender, instance, **kwargs):
    act = 'удалил'
    notification = Notification(owner=instance.owner, subject=f'заказ {instance.marker}', action=act, subject_owner=instance.owner)
    notification.save()


@receiver(post_save, sender=Product)
def model_post_save(sender, instance, **kwargs):
    product = Product.objects.get(pk=instance.pk)
    if Order.objects.filter(product=instance).count():
        print(Order.objects.filter(product=instance).count())
        a = Order.objects.filter(product=instance)
        for i in a:
            print(i)
        order = Order.objects.get(product=instance)
        total_price = sum([i.full_price for i in order.product.all()])
        order.total_price = total_price
        order.total_price_rub = order.total_price * order.exchange_for_client

        total_price_company = sum([i.full_price_company for i in order.product.all()])
        order.total_price_company = total_price_company
        order.total_price_rub_company = order.total_price_company * order.exchange_for_company
        order.save()
    print('это старый сигнал!')


@receiver(pre_delete, sender=Product)
def model_pre_delete(sender, instance, **kwargs):
    product = Product.objects.get(pk=instance.pk)
    if Order.objects.filter(product=product).count() == 0:
        pass
    else:
        order = Order.objects.get(product=product)
        order.product.remove(product)
        total_price = sum([i.full_price for i in order.product.all()])
        order.total_price = total_price
        order.total_price_rub = order.total_price * order.exchange_for_client
        order.save()


@receiver(pre_delete, sender=Order)
def model_pre_delete(sender, instance, **kwargs):
    order = Order.objects.get(pk=instance.pk)
    if not order.product:
        pass
    else:
        for product in order.product.all():
            product.delete()


class ReadOnlyException(Exception):
    pass

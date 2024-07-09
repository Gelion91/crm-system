import os
import django.dispatch
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

from core.models import Order, Clients, Product, Logistics, Notification


@receiver(post_save, sender=Logistics)
def create_logistic(sender, instance, created, **kwargs):
    act = 'изменил'
    if created:
        act = 'создал'
    notification = Notification(owner=instance.owner, subject=f'доставку {instance.marker}', action=act)
    notification.save()


@receiver(post_save, sender=Logistics)
def change_logistic(sender, instance, created, **kwargs):
    if not created:
        if instance.sendings.all():
            sending = instance.sendings.first()
            print(sending)
            sending.weight = sum(i.weight for i in sending.logistics.all())
            sending.volume = sum(i.volume for i in sending.logistics.all())
            sending.places = sum(i.places for i in sending.logistics.all())
            sending.save()


@receiver(post_delete, sender=Logistics)
def delete_logistic(sender, instance, **kwargs):
    act = 'удалил'
    notification = Notification(owner=instance.owner, subject=f'доставку {instance.marker}', action=act)
    notification.save()


@receiver(post_save, sender=Product)
def create_product(sender, instance, created, **kwargs):
    act = 'изменил'
    if created:
        act = 'создал'
    notification = Notification(owner=instance.owner, subject=f'продукт {instance.product_marker}({instance.name})', action=act)
    notification.save()


@receiver(post_delete, sender=Product)
def create_product(sender, instance, **kwargs):
    act = 'удалил'
    notification = Notification(owner=instance.owner, subject=f'продукт {instance.product_marker}({instance.name})', action=act)
    notification.save()


@receiver(post_save, sender=Order)
def create_product(sender, instance, created, **kwargs):
    act = 'изменил'
    if created:
        act = 'создал'
    notification = Notification(owner=instance.owner, subject=f'заказ {instance.marker}', action=act)
    notification.save()


@receiver(post_delete, sender=Order)
def create_product(sender, instance, **kwargs):
    act = 'удалил'
    notification = Notification(owner=instance.owner, subject=f'заказ {instance.marker}', action=act)
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

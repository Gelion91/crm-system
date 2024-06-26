import os
import django.dispatch
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

from core.models import Order, Clients, Product, Logistics


# @receiver(post_save, sender=Logistics)
# def create_logistic(sender, instance, created, **kwargs):
#     logistic = Logistics.objects.get(pk=instance.pk)
#     print(logistic)
#     print(logistic.product.all())


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

import os

from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

from core.models import Order, Clients, Product
from crm import settings


# @receiver(pre_delete, sender=Order)
# @receiver(pre_delete, sender=Clients)
# @receiver(pre_save, sender=Order)
# @receiver(pre_save, sender=Clients)
# def model_pre_change(sender, **kwargs):
#     if os.path.isfile(settings.READ_ONLY_FILE):
#         raise ReadOnlyException('Model in read only mode, cannot save')


@receiver(post_save, sender=Product)
def model_post_save(sender, instance, **kwargs):
    product = Product.objects.get(pk=instance.pk)
    print(product)
    if Order.objects.filter(product=instance).count():
        order = Order.objects.get(product=instance)
        print(order)
        total_price = sum([i.full_price for i in order.product.all()])
        order.total_price = total_price
        order.total_price_rub = order.total_price * order.exchange_for_client
        order.save()


@receiver(pre_delete, sender=Product)
def model_pre_delete(sender, instance, **kwargs):
    product = Product.objects.get(pk=instance.pk)
    order = Order.objects.get(product=product)
    order.product.remove(product)
    total_price = sum([i.full_price for i in order.product.all()])
    order.total_price = total_price
    order.total_price_rub = order.total_price * order.exchange_for_client
    order.save()


class ReadOnlyException(Exception):
    pass
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from core.models import Logistics


class Sending(models.Model):
    AUTO = "Авто"
    AUTO_EXPRESS = "Авто-экспресс"
    RAIL = "Жд"
    AVIA = "Авиа"

    DELIVERY_CHOICES = [
        (AUTO, "Авто"),
        (AUTO_EXPRESS, "Авто-экспресс"),
        (RAIL, "Жд"),
        (AVIA, "Авиа"),
    ]

    marker = models.CharField(max_length=100, verbose_name='Номер отправления')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    logistics = models.ManyToManyField(Logistics, verbose_name='Грузы', related_name='sendings')
    weight = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Вес, кг.', default=0)
    volume = models.DecimalField(decimal_places=3, max_digits=100, verbose_name='Объем', default=0)
    tariff = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Стоимость доставки $', default=0)
    order_price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Стоимость товаров в заказах ¥',
                                      default=0)
    delivery = models.CharField(max_length=100, choices=DELIVERY_CHOICES, default='Авто', null=False,
                                verbose_name='Тип отправления')
    places = models.IntegerField(verbose_name='Количество мест', default=1)
    carrier = models.ForeignKey('Carriers', verbose_name='Перевозчик', related_name='carrier',
                                on_delete=models.SET_NULL, null=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    first_step = models.BooleanField(verbose_name='Отправлен', default=False)
    second_step = models.BooleanField(verbose_name='В Москве', default=False)

    class Meta:
        verbose_name = 'Отправка'
        verbose_name_plural = 'Отправки'
        ordering = ['-id']

    def __str__(self):
        if self.marker:
            return self.marker
        return "без имени"

    def get_absolute_url(self):
        return reverse('sendings', kwargs={'sending_id': self.pk})


class Carriers(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название перевозчика')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        if self.name:
            return self.name
        return "без имени"

    def get_absolute_url(self):
        return reverse('carrier', kwargs={'carrier_id': self.pk})


class NotesSending(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Менеджер')
    sending = models.ForeignKey(Sending, on_delete=models.SET_NULL, null=True, verbose_name='Отправка',
                                related_name='sending_notes')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['id']

    def __str__(self):
        """
        String for representing the Model object.
        """
        if self.owner:
            return self.owner.username
        else:
            return 'без имени'

    def get_absolute_url(self):
        return reverse('note', kwargs={'note_id': self.pk})

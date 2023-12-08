import datetime

from django.contrib.auth.models import User
from django.db import models
from autoslug.fields import AutoSlugField
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import django.dispatch


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Товар')
    url = models.CharField(max_length=500, verbose_name='Ссылка на продавца')
    arrive = models.BooleanField(verbose_name='Прибыл на склад')
    paid = models.BooleanField(verbose_name='Оплачен')
    photo = models.ImageField(upload_to='core/image', verbose_name='Изображение', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Цена', default=0)
    fraht = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Стоимость доставки по Китаю', default=0)
    quantity = models.IntegerField(verbose_name='Количество мест', default=0)
    full_price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Общая цена', default=0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']

    def __str__(self):
        """
        String for representing the Model object.
        """
        if self.name:
            return self.name
        return self.url

    def save(self, *args, **kwargs):
        self.full_price = self.price + self.fraht
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('client', kwargs={'product_id': self.pk})


class Clients(models.Model):

    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, null=True, verbose_name='Фамилия')
    phone = PhoneNumberField(null=True, verbose_name='Номер телефона')
    slug = AutoSlugField(populate_from='name', db_index=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    result = models.BooleanField(verbose_name='Согласен')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-id']

    def __str__(self):
        """
        String for representing the Model object.
        """
        if self.name:
            return f"{self.name} {self.surname}"
        return "без имени"

    def get_absolute_url(self):
        return reverse('client', kwargs={'client_id': self.pk})


class Order(models.Model):
    REGISTRATION = "Оформление"
    PAYMENT = "На оплату"
    COMPLETE = "Завершен"

    ORDER_CHOICES = [
        (REGISTRATION, "Оформление"),
        (PAYMENT, "Оплата"),
        (COMPLETE, "Выполнен"),
    ]
    client = models.ForeignKey(Clients, on_delete=models.SET_NULL, null=True, verbose_name='Клиент')
    marker = models.CharField(max_length=100, verbose_name='Маркировка')
    product = models.ManyToManyField(Product, verbose_name='Товары')
    slug = AutoSlugField(populate_from='marker', db_index=True)
    weight = models.FloatField(verbose_name='Вес кг.')
    exchange_for_client = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Курс ¥ для клиента', default=0)
    exchange_for_company = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Курс ¥ для компании', default=0)
    arrive_price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Цена доставки $', default=0)
    status = models.CharField(max_length=100, choices=ORDER_CHOICES, default='re', null=False, verbose_name='Статус')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    total_price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Итоговая цена ¥', default=0)
    total_price_rub = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Итоговая цена ₽', default=0)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']

    def __str__(self):
        """
        String for representing the Model object.
        """
        if self.marker:
            return self.marker
        return "без имени"

    def save(self, *args, **kwargs):
        try:
            total_price = sum(i.full_price for i in Order.objects.get(pk=self.pk).product.all())
            self.total_price = 0
            self.total_price = total_price
            self.total_price_rub = self.total_price * self.exchange_for_client
        except:
            pass
        super(Order, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('order', kwargs={'order_id': self.pk})
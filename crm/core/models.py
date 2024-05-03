from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import validate_image_file_extension
from django.db import models
from autoslug.fields import AutoSlugField
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Product(models.Model):
    product_marker = models.CharField(max_length=100, verbose_name='маркировка товара', null=True)
    name = models.CharField(max_length=100, verbose_name='Наименование')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    number_order = models.CharField(max_length=100, verbose_name='Номер заказа', blank=True)
    url = models.CharField(max_length=500, verbose_name='Ссылка на продавца', blank=True)
    arrive = models.BooleanField(verbose_name='Прибыл на склад')
    paid = models.BooleanField(verbose_name='Оплачен')
    price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Цена для клиента ¥', default=0)
    price_company = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Цена для компании ¥', default=0)
    margin_product = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Наценка ¥', default=0)
    fraht = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Доставка по Китаю для клиента ¥',
                                default=0)
    fraht_company = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Доставка по Китаю для '
                                                                                       'компании ¥', default=0)
    quantity = models.IntegerField(verbose_name='Количество', default=1)
    full_price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Общая цена для клиента ¥', default=0)
    full_price_company = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Общая цена для компании ¥', default=0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']

    def __str__(self):
        """
        String for representing the Model object.
        """
        if self.product_marker:
            return self.product_marker
        return self.name

    def save(self, *args, **kwargs):
        self.full_price = self.price + self.fraht
        self.full_price_company = self.price_company + self.fraht_company
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('client', kwargs={'product_id': self.pk})


class ImagesProduct(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/', validators=[validate_image_file_extension])

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('core', kwargs={'image_id': self.pk})


class PackedImagesProduct(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='packed_images')
    image = models.ImageField(upload_to='packed_images/', validators=[validate_image_file_extension])

    class Meta:
        verbose_name = 'Изображение упакованного продукта'
        verbose_name_plural = 'Изображения упакованного продукта'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('core', kwargs={'packed_image_id': self.pk})


class Clients(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, null=True, verbose_name='Фамилия', blank=True)
    phone = PhoneNumberField(null=True, verbose_name='Номер телефона', unique=True, blank=True)
    messanger = models.TextField(max_length=500, null=True, verbose_name='Примечание', blank=True)
    deposit = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Счет', default=0)
    slug = AutoSlugField(populate_from='name', db_index=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    result = models.BooleanField(verbose_name='Согласен', default=True)
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
        if self.surname:
            return f"{self.name} {self.surname}"
        elif not self.surname:
            return f"{self.name}"
        return "без имени"

    def get_absolute_url(self):
        return reverse('client', kwargs={'client_id': self.pk})


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    accounts = models.CharField(max_length=100, verbose_name='Аккаунт')

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['-id']

    def __str__(self):
        """
        String for representing the Model object.
        """
        if self.accounts:
            return self.accounts
        return "без аккаунта"

    def get_absolute_url(self):
        return reverse('account', kwargs={'account_id': self.pk})


class Order(models.Model):
    REGISTRATION = "Оформление"
    PAYMENT = "Ожидает отправки"
    COMPLETE = "Завершен"

    ALFA_BANK = "Альфа-банк"
    SBER = "Сбер"
    TINKOFF = "Тинькофф"
    TIMOFEEV = "Тимофеев"
    CASH = "Наличные"
    IP = "Расчетный счет"

    IGOR = "Игорь Смирнов"
    SERGEY = "Сергей Тимофеев"
    MARIA = "Мария"

    WHO_TAKE_MONEY = [
        (IGOR, "Игорь Смирнов"),
        (SERGEY, "Сергей Тимофеев"),
        (MARIA, "Мария"),
    ]

    ORDER_CHOICES = [
        (REGISTRATION, "Оформление"),
        (PAYMENT, "Ожидает отправки"),
        (COMPLETE, "Выполнен"),
    ]

    PAID_METHOD = [
        (ALFA_BANK, "Альфа-банк Игорь"),
        (SBER, "Сбер Мария"),
        (TINKOFF, "Тинькофф Игорь"),
        (TIMOFEEV, "Тимофеев"),
        (CASH, "Наличные"),
        (IP, "Расчетный счет(ИП)"),
    ]

    client = models.ForeignKey(Clients, on_delete=models.SET_NULL, null=True, verbose_name='Клиент')
    marker = models.CharField(max_length=100, verbose_name='Маркировка заказа')
    product = models.ManyToManyField(Product, verbose_name='Товары', related_name='order')
    slug = AutoSlugField(populate_from='marker', db_index=True)
    exchange_for_client = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Курс ¥ для клиента',
                                              default=0)
    exchange_for_company = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Курс ¥ для компании',
                                               default=0)
    status = models.CharField(max_length=100, choices=ORDER_CHOICES, default='Оформление', null=False,
                              verbose_name='Статус')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name='Аккаунт')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    margin = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Наценка ¥', default=0)
    total_price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Итоговая цена для клиента ¥', default=0)
    total_price_rub = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Итоговая цена для клиента ₽', default=0)
    total_price_company = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Итоговая цена для компании ¥', default=0)
    total_price_rub_company = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Итоговая цена для компании ₽', default=0)
    profit = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Прибыль', default=0)
    paid_method = models.CharField(max_length=100, choices=PAID_METHOD, default='Наличные', null=False,
                                   verbose_name='Способ оплаты')
    takemoney = models.CharField(max_length=100, choices=WHO_TAKE_MONEY, verbose_name='Кто принял оплату', blank=True)
    result = models.BooleanField(verbose_name='Выполнен', default=False)

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
        # if self.exchange_for_client:
        #     self.exchange_for_company = self.exchange_for_client - Decimal(0.3)
        if self.status == "Завершен":
            self.result = True
        else:
            self.result = False
        try:
            total_price = sum(i.full_price for i in Order.objects.get(pk=self.pk).product.all())
            total_price_company = sum(i.full_price_company for i in Order.objects.get(pk=self.pk).product.all())
            self.total_price = 0
            self.total_price = total_price
            self.total_price_rub = self.total_price * self.exchange_for_client
            self.total_price_company = 0
            self.total_price_company = total_price_company
            self.total_price_rub_company = self.total_price_company * self.exchange_for_company

            self.profit = self.total_price_rub - self.total_price_rub_company
        except:
            pass
        super(Order, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('order', kwargs={'order_id': self.pk})


class Logistics(models.Model):
    SIMPLY = "Простая"
    SHEATHING = "Обрешетка"
    BOX = "Ящик"
    BAG = "Скотч-мешок-скотч"

    PACKAGE_CHOICES = [
        (SIMPLY, "Простая"),
        (BAG, "Скотч-мешок-скотч"),
        (SHEATHING, "Обрешетка"),
        (BOX, "Ящик"),
    ]

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

    marker = models.CharField(max_length=100, verbose_name='Маркировка груза')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    product = models.ManyToManyField(Product, verbose_name='Товары', related_name='logistics')
    height = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Высота, см.', default=0)
    width = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Ширина, см.', default=0)
    lenght = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Длина, см.', default=0)
    weight = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Вес, кг.', default=0)
    volume = models.DecimalField(decimal_places=3, max_digits=100, verbose_name='Объем', default=0)
    density = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Плотность', default=0)
    tariff = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Стоимость доставки $', default=0)
    order_price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Стоимость товаров в заказах ¥',
                                      default=0)
    insurance = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Стоимость страховки $', default=0)
    package = models.CharField(max_length=100, choices=PACKAGE_CHOICES, default='simply', null=False,
                               verbose_name='Упаковка')
    extra_package = models.TextField(max_length=500, null=True, verbose_name='Примечание по упаковке', blank=True)
    package_price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Стоимость упаковки $', default=0)
    full_price = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Общая стоимость', default=0)
    delivery = models.CharField(max_length=100, choices=DELIVERY_CHOICES, default='Авто', null=False,
                                verbose_name='Тип отправления')
    places = models.IntegerField(verbose_name='Количество мест', default=1)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    first_step = models.BooleanField(verbose_name='Отправлен', default=False)
    second_step = models.BooleanField(verbose_name='В Москве', default=False)
    third_step = models.BooleanField(verbose_name='Получен клиентом', default=False)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ['-id']

    def __str__(self):
        """
        String for representing the Model object.
        """
        if self.marker:
            return self.marker
        return "без имени"

    # def save(self, *args, **kwargs):
    #     if self.product.all():
    #         print(self.product)
    #         self.order_price = sum(product.full_price for product in self.product.all())
    #     super(Logistics, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('logistic', kwargs={'logistic_id': self.pk})


class ImagesLogistics(models.Model):
    logistic = models.ForeignKey(Logistics, default=None, on_delete=models.CASCADE, related_name='logistic_images')
    image = models.ImageField(upload_to='logistic_images/', validators=[validate_image_file_extension])

    class Meta:
        verbose_name = 'Изображение упакованного груза'
        verbose_name_plural = 'Изображения упакованного груза'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('core', kwargs={'logistic_image_id': self.pk})
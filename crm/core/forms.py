from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML, Button
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
from django.forms import ModelForm, CheckboxSelectMultiple, SelectMultiple, TextInput, MultipleHiddenInput, \
    PasswordInput, modelformset_factory, BaseFormSet, HiddenInput, inlineformset_factory, ClearableFileInput
from django.utils.html import format_html

from core.models import Order, Clients, Product, ImagesProduct, Logistics
from django import forms


class AddOrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))

    class Meta:
        model = Order
        fields = ['client', 'marker']


class UpdateOrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))
        self.fields["total_price"].disabled = True
        self.fields["total_price_rub"].disabled = True
        self.fields["total_price_company"].disabled = True
        self.fields["total_price_rub_company"].disabled = True


    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('product', 'owner', 'margin')


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(ModelForm):
    image = forms.ImageField(widget=MultipleFileInput, validators=[validate_image_file_extension], required=False)
    DELETE = forms.BooleanField(initial=True, widget=HiddenInput)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('full_price', 'DELETE', 'logistics', 'margin_product')

    def clean_image(self):
        data = self.cleaned_data['image']
        if data:
            valid_formats = ['png', 'jpeg']
            if not any([True if data.name.endswith(i) else False for i in valid_formats]):
                raise ValidationError(f'{data.name} is not a valid image format')

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data


class ImageForm(ModelForm):
    class Meta:
        model = ImagesProduct
        fields = '__all__'


ProductImageInlineFormset = inlineformset_factory(
    Product,
    ImagesProduct,
    fields='__all__',
    extra=0,
    form=ImageForm,
)


class ProductFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProductFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Div(Div('product_marker', css_class='col-6'),
                Div('name', css_class='col-6'), css_class='row'),
            Div(Div('url', css_class='col-12'), css_class='row'),
            Div(Div('number_order', css_class='col-12'), css_class='row'),
            Div(Div('price', css_class='col-6'),
                Div('price_company', css_class='col-6'), css_class='row'),
            Div(Div('quantity', css_class='col-12'), css_class='row'),
            Div(Div('fraht', css_class='col-12'), css_class='row'),
            Div(Div('fraht_company', css_class='col-12'), css_class='row'),
            Div(Div('arrive', css_class='col-6'),
                Div('paid', css_class='col-6'), css_class='row'),
            Div('DELETE', css_class='input-small'),
            HTML("""<hr>""")
        )
        self.render_required_fields = True
        self.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))


ProductFormSet = modelformset_factory(
    Product, fields=("name", "url", "price", "fraht", "quantity", "arrive", "paid",), extra=0, can_delete=True
)


class FilterName(forms.Form):
    client = forms.CharField(label='Клиент', max_length=200)


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Пароль'}))


class ImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))

    class Meta:
        model = ImagesProduct
        fields = '__all__'


class DeliveryAddForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DeliveryAddForm, self).__init__(*args, **kwargs)
        qs1 = Product.objects.filter(paid=True, arrive=True, logistics=None)
        if self.initial:
            qs2 = Product.objects.filter(logistics=self.instance.pk)
        else:
            qs2 = Product.objects.none()
        queryset = (qs1 | qs2).distinct()
        if self.initial:
            qs1 = Product.objects.prefetch_related('logistics').filter(paid=True, arrive=True).filter(
                logistics__product__isnull=True)
            qs2 = self.instance.product.all()
            self.fields["product"].queryset = (qs1 | qs2).distinct()
        else:
            self.fields["product"].queryset = Product.objects.prefetch_related('logistics').filter(paid=True,
                                                                                                   arrive=True).filter(
                logistics__product__isnull=True)
        # self.fields['product'].widget = CheckboxSelectMultiple()
        self.fields['product'].widget = FilteredSelectMultiple("Товары", is_stacked=False)
        self.fields['product'].queryset = queryset
        self.fields['product'].label = ''
        self.fields['product'].required = False
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))
        self.helper.layout = Layout(
            'marker',
            Div(Div('product', css_class='col-12'), css_class='row'),

            Div(Div('package', 'delivery', css_class='col-12'), css_class='row'),
            Div(Div('weight', css_class='col-4'),
                Div('volume', css_class='col-4'),
                Div('density', css_class='col-4'), css_class='row'),

            Div(Div('tariff', css_class='col-6'),
                Div('insurance', css_class='col-6'), css_class='row'),

            Div(Div('package_price', css_class='col-4'),
                Div('full_price', css_class='col-4'),
                Div('order_price', css_class='col-4'), css_class='row')
        )

    class Meta:
        model = Logistics
        fields = '__all__'
        exclude = ('height', 'width', 'lenght')

    class Media:
        css = {
            'all': ('/static/admin/css/widgets.css',),
        }
        js = ('/admin/jsi18n', 'defer', 'core/js/main.js')


def render_js(cls):
    fmt = '<script src="{}"></script>'
    formats = {
        'defer': '<script defer src="{}"></script>'
    }

    for path in cls._js:
        if path in formats:
            fmt = formats[path]
            break

    return [
        format_html(
            fmt,
            cls.absolute_path(path)
        ) for path in cls._js if path not in formats
    ]


forms.widgets.Media.render_js = render_js


class DeliveryForm(forms.Form):
    SIMPLY = "Простая"
    SHEATHING = "Обрешетка"
    BOX = "Ящик"

    PACKAGE_CHOICES = [
        (SIMPLY, "Простая"),
        (SHEATHING, "Обрешетка"),
        (BOX, "Ящик"),
    ]

    UNDELIVERED = "undelivered"
    IN_STOCK = "in_stock"
    IN_MOSCOW = "in_moscow"
    DELIVERED = "delivered"

    DELIVERY_CHOICES = [
        (UNDELIVERED, "Не доставлено"),
        (IN_STOCK, "На складе Китай"),
        (IN_MOSCOW, "В Москве"),
        (DELIVERED, "Доставлено"),
    ]

    qs1 = Product.objects.filter(paid=True, arrive=True, logistics=None)
    qs2 = Product.objects.none()
    queryset = (qs1 | qs2).distinct()

    marker = forms.CharField(max_length=100, label='Маркировка груза')
    products = forms.ModelMultipleChoiceField(queryset=queryset,
                                              widget=CheckboxSelectMultiple(), label='Товары')
    weight = forms.DecimalField(decimal_places=2, max_digits=100, label='Вес, кг.', initial=0)
    volume = forms.DecimalField(decimal_places=3, max_digits=100, label='Объем', initial=0)
    density = forms.DecimalField(decimal_places=2, max_digits=100, label='Плотность', initial=0)
    tariff = forms.DecimalField(decimal_places=2, max_digits=100, label='Тариф', initial=0)
    order_price = forms.DecimalField(decimal_places=2, max_digits=100, label='Стоимость товаров в заказах ¥',
                                     initial=0)
    insurance = forms.DecimalField(decimal_places=2, max_digits=100, label='Страховка', initial=0)
    package = forms.ChoiceField(choices=PACKAGE_CHOICES, initial='simply',
                                label='Упаковка')
    package_price = forms.DecimalField(decimal_places=2, max_digits=100, label='Стоимость упаковки', initial=0)
    full_price = forms.DecimalField(decimal_places=2, max_digits=100, label='Общая стоимость', initial=0)
    delivery = forms.ChoiceField(choices=DELIVERY_CHOICES, initial='undelivered',
                                 label='Статус отправления')

    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))
        # if self.initial:
        #     qs1 = Order.objects.prefetch_related('delivery').filter(status='Завершен').filter(delivery__order__isnull=True)
        #     qs2 = self.instance.order.all()
        #     self.fields["order"].queryset = (qs1 | qs2).distinct()
        # else:
        #     self.fields["order"].queryset = Order.objects.prefetch_related('delivery').filter(status='Завершен').filter(
        #         delivery__order__isnull=True)

        self.helper.layout = Layout(
            'marker',
            Div(Div('products', css_class='col-8'),
                Div('package', 'delivery', css_class='col-4'), css_class='row'),
            Div(Div('weight', css_class='col-4'),
                Div('volume', css_class='col-4'),
                Div('density', css_class='col-4'), css_class='row'),

            Div(Div('tariff', css_class='col-6'),
                Div('insurance', css_class='col-6'), css_class='row'),

            Div(Div('package_price', css_class='col-4'),
                Div('full_price', css_class='col-4'),
                Div('order_price', css_class='col-4'), css_class='row')
        )

    # def clean(self):
    #     cleaned_data = super().clean()
    #     origin = cleaned_data.get("origin")
    #     destination = cleaned_data.get("destination")
    #     need_return = cleaned_data.get("need_return")
    #     return_at = cleaned_data.get("return_at")
    #     msg = "Нет такого города, попробуйте еще раз."
    #     if not Cities.objects.filter(name__icontains=origin):
    #         self.add_error('origin', msg)
    #     if not Cities.objects.filter(name__icontains=destination):
    #         self.add_error('destination', msg)
    #     if need_return and not return_at:
    #         self.add_error('return_at', 'Необходимо выбрать дату обратного пути.')

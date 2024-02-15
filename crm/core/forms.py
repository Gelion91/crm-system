from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML, Button
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, CheckboxSelectMultiple, SelectMultiple, TextInput, MultipleHiddenInput, \
    PasswordInput, modelformset_factory, BaseFormSet, HiddenInput, inlineformset_factory
from core.models import Order, Clients, Product, ImagesProduct, Logistics
from django import forms

from core.widgets import CustomClearableFileInput


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
        fields = '__all__'
        exclude = ('product', 'owner', 'total_price', 'total_price_rub', 'result')


class UpdateOrderForm(AddOrderForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["total_price"].disabled = True
        self.fields["total_price_rub"].disabled = True

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('product', 'owner')


class ProductForm(ModelForm):
    DELETE = forms.BooleanField(initial=True, widget=HiddenInput)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))
        self.layout = (Layout(
            Div(Div('name', css_class='col-6'),
                Div('price', css_class='col-6'), css_class='row'),
            'url',
            Div(css_class='row'),
            Div('fraht', css_class='col-8'),
            Div('quantity', css_class='col-4'),
            Div('arrive', css_class='col-8'),
            Div('paid', css_class='col-4'),
            Div(fields='photo', ),
        ),)

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'photo': CustomClearableFileInput
        }
        exclude = ('full_price', 'DELETE')


class ProductFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProductFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Div(css_class='row'),
            Div('name', css_class='col-6'),
            Div('price', css_class='col-6'),
            'url',
            Div(css_class='row'),
            Div('fraht', css_class='col-8'),
            Div('quantity', css_class='col-4'),
            Div('arrive', css_class='col-8'),
            Div('paid', css_class='col-4'),
            'photo', Div('DELETE', css_class='input-small'),
            HTML("""<hr>""")
        )
        self.render_required_fields = True
        self.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))


ProductFormSet = modelformset_factory(
    Product, fields=("name", "url", "price", "fraht", "quantity", "arrive", "paid", 'photo',), extra=0, can_delete=True
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
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))
        self.fields["order"].widget = forms.widgets.CheckboxSelectMultiple()
        if self.initial:
            qs1 = Order.objects.prefetch_related('delivery').filter(status='Завершен').filter(delivery__order__isnull=True)
            qs2 = self.instance.order.all()
            self.fields["order"].queryset = (qs1 | qs2).distinct()
        else:
            self.fields["order"].queryset = Order.objects.prefetch_related('delivery').filter(status='Завершен').filter(
                delivery__order__isnull=True)

        self.helper.layout = Layout(
            Div(Div('order', css_class='col-6'),
                Div('package', 'delivery', css_class='col-6'), css_class='row'),

            Div(Div('height', css_class='col-4'),
                Div('width', css_class='col-4'),
                Div('lenght', css_class='col-4'), css_class='row'),

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

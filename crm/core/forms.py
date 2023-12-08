from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, CheckboxSelectMultiple, SelectMultiple, TextInput, MultipleHiddenInput, \
    PasswordInput, modelformset_factory, BaseFormSet, HiddenInput
from core.models import Order, Clients, Product
from django import forms


class AddClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields["name"].widget.attrs.update({"class": "form__field"})

    class Meta:
        model = Clients
        fields = '__all__'
        exclude = ('owner',)


class AddOrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn btn-light'))

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('product', 'owner', 'total_price', 'total_price_rub')


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

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn btn-light'))
        self.layout = Layout(
            Div(Div('name', css_class='col-6'),
                Div('price', css_class='col-6'), css_class='row'),
            'url',
            Div(css_class='row'),
            Div('fraht', css_class='col-8'),
            Div('quantity', css_class='col-4'),
            Div('arrive', css_class='col-8'),
            Div('paid', css_class='col-4'),
            'photo', )

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('full_price',)
        # widgets = {
        #     'photo': UploadedFileInput(),
        # }


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
        )
        self.render_required_fields = True
        self.add_input(Submit("submit", 'Сохранить', css_class='btn btn-light'))


# class BaseArticleFormSet(BaseFormSet):
#     deletion_widget = HiddenInput
#
#     def __init__(self, queryset=None):
#         super().__init__()
#         self.queryset = queryset


ProductFormSet = modelformset_factory(
    Product, fields=("name", "url", "price", "fraht", "quantity", "arrive", "paid", 'photo',), extra=0, can_delete=True
)


class FilterName(forms.Form):
    client = forms.CharField(label='Клиент', max_length=200)


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Пароль'}))

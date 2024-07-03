from crispy_forms.bootstrap import InlineRadios, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML, Button
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
from django.forms import ModelForm, CheckboxSelectMultiple, SelectMultiple, TextInput, MultipleHiddenInput, \
    PasswordInput, modelformset_factory, BaseFormSet, HiddenInput, inlineformset_factory, ClearableFileInput, \
    ChoiceField, RadioSelect
from django.utils.html import format_html

from core.models import Order, Clients, Product, ImagesProduct, Logistics, PackedImagesProduct, Account, NotesProduct, \
    NotesDelivery
from django import forms

from sendings.models import Sending, Carriers, NotesSending


class SimplySendingForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(SimplySendingForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Sending
        fields = ['marker', 'weight', 'volume']


class SendingCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):

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
        self.current_user = kwargs.pop('current_user', None)
        super(SendingCreateForm, self).__init__(*args, **kwargs)
        qs1 = Logistics.objects.filter(sendings=None)
        if self.initial:
            qs2 = Logistics.objects.filter(sendings=self.instance.pk)
        else:
            qs2 = Logistics.objects.none()
        queryset = (qs1 | qs2).distinct()
        if self.initial:
            qs1 = Logistics.objects.prefetch_related('sendings').filter(
                sendings__logistics__isnull=True)
            qs2 = self.instance.logistics.all()
            self.fields["logistics"].queryset = (qs1 | qs2).distinct()
        else:
            self.fields["logistics"].queryset = Logistics.objects.filter(sendings=None)
        self.fields['logistics'].widget = CheckboxSelectMultiple(choices=self.fields["logistics"].queryset)
        # self.fields['product'].widget = FilteredSelectMultiple("Товары", is_stacked=False)
        self.fields['delivery'].widget = RadioSelect(choices=DELIVERY_CHOICES)
        if self.current_user.is_superuser or self.current_user.groups.filter(name='logist'):
            self.fields['logistics'].queryset = queryset
        else:
            self.fields['logistics'].queryset = queryset.filter(owner=self.current_user)
        self.fields['logistics'].label = ''
        self.fields['logistics'].required = False
        self.fields["logistics"].widget.attrs.update({"class": "form-check-inline"})
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", 'Сохранить', css_class='btn-secondary'))
        self.helper.layout = Layout(
            'marker',
            InlineRadios('logistics', css_class='col-12 product_select',),
            Div(Div('carrier', StrictButton('Добавить перевозчика', name='add_carrier', css_class='btn-secondary'), css_class='col-6'),
                Div('delivery', css_class='col-6'), css_class='row'),
            Div(Div('weight', css_class='col-6'),
                Div('volume', css_class='col-6'), css_class='row'),
            Div(Div('tariff', css_class='col-6'),
                Div('places', css_class='col-6'), css_class='row'),
            Div(Div('order_price', css_class='col-12'), css_class='row'),
        )

    class Meta:
        model = Sending
        fields = '__all__'
        exclude = ('first_step', 'second_step', 'owner')


class SendingNotesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = NotesDelivery
        fields = '__all__'
        exclude = ('owner', 'sending')


class CarrierAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.layout = Layout(
            'name',
            'comment',
            Submit(value='Добавить перевозчика', name='submit_carrier', css_class='btn-secondary')
        )

    class Meta:
        model = Carriers
        fields = '__all__'


class SendingNotesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = NotesSending
        fields = '__all__'
        exclude = ('owner', 'sending')

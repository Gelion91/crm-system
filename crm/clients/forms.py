from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from clients.models import Comments
from core.models import  Clients
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
        self.fields["phone"].widget.attrs.update(
            {'placeholder': 'Номер телефона в формате +7...'})
        self.fields["messanger"].widget.attrs.update(
            {'placeholder': 'Поле для заметок. Например номер wechat или whatsapp...'})

    class Meta:
        model = Clients
        fields = '__all__'
        exclude = ('owner', 'comment', 'deposit')


class FilterName(forms.Form):
    client = forms.CharField(label='Клиент', max_length=200)


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'whiteForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Comments
        fields = '__all__'
        exclude = ('owner', 'client')

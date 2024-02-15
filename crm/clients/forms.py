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

    class Meta:
        model = Clients
        fields = '__all__'
        exclude = ('owner', 'comment')


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

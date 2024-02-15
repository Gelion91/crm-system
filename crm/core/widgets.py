from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    initial_text = 'Текущее изображение'

    input_text = 'Изменить'

    clear_checkbox_label = 'Очистить'

    template_with_initial = (
        '<span>%(initial_text)s</span>:'
        '<a href="%(initial_url)s">%(initial)s</a>'
        '%(clear_template)s<br/><span>%(input_text)s</span>: %(input)s'
    )

    template_with_clear = '%(clear)s'
    '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

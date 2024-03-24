from django.core.exceptions import ValidationError


def custom_validator(value):
    print(value)
    print(1111)
    valid_formats = ['png', 'jpeg']
    if not any([True if value.name.endswith(i) else False for i in valid_formats]):
        raise ValidationError(f'{value.name} is not a valid image format')
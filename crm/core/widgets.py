import posixpath

from django import forms
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


def thumbnail(image_path, width, height):
    absolute_url = posixpath.join(settings.MEDIA_URL, image_path)
    return f'<img src="{absolute_url}" alt="{image_path}" class="django-widget-img" ' \
           f'width={width} height={height} loading=lazy />', absolute_url


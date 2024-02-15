from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from core.models import Clients


class Comments(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Менеджер')
    client = models.ForeignKey(Clients, on_delete=models.SET_NULL, null=True, verbose_name='Клиент')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-id']

    def __str__(self):
        """
        String for representing the Model object.
        """
        if self.owner:
            return self.owner.username
        else:
            return 'без имени'

    def get_absolute_url(self):
        return reverse('comment', kwargs={'comment_id': self.pk})

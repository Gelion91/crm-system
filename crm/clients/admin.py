from django.contrib import admin

from clients.models import Comments
from core.models import Clients


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'date_create', 'owner')
    search_fields = ('name', 'owner__username',)


admin.site.register(Comments)
admin.site.register(Clients, ClientsAdmin)

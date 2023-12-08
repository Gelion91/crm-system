from django.contrib import admin

from .models import Clients, Order, Product


# Register your models here.

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'arrive', 'paid', 'photo')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'marker', 'weight', 'exchange_for_client', 'exchange_for_company', 'arrive_price', 'status')
    search_fields = ['client', 'marker', 'status']


admin.site.register(Clients, ClientsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)

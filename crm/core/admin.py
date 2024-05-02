from django.contrib import admin

from .models import Clients, Order, Product, Logistics, Account


# Register your models here.

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'arrive', 'paid')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'marker', 'exchange_for_client', 'exchange_for_company', 'status')
    search_fields = ['client', 'marker', 'status']


admin.site.register(Clients, ClientsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Logistics)
admin.site.register(Account)
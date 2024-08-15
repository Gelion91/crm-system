

from django.contrib import admin

from .models import Clients, Order, Product, Logistics, Account, Invoices


# Register your models here.

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'date_create')
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_marker', 'name', 'url', 'arrive', 'paid', 'date_create')
    search_fields = ['product_marker', 'name', 'date_create']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'marker', 'exchange_for_client', 'exchange_for_company', 'status', 'date_create')
    search_fields = ['client', 'marker', 'status']


admin.site.register(Clients, ClientsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Logistics)
admin.site.register(Account)
admin.site.register(Invoices)
from django.urls import path

from clients import views

app_name = 'clients'

urlpatterns = [
    path('clients/', views.ClientsListView.as_view(), name='home'),
]
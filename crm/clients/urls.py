from django.urls import path

from clients import views
from clients.views import ClientDetail, delete_comment

app_name = 'clients'

urlpatterns = [
    path('clients/', views.ClientsListView.as_view(), name='home'),
    path('clients/my_clients', views.MyClientsListView.as_view(), name='my_clients'),
    path('clients/active_clients', views.ActiveClientsListView.as_view(), name='active'),
    path('clients/update_client/<int:client_id>/', views.UpdateClient.as_view(), name='upd'),
    path('clients/addclient/', views.AddClient.as_view(), name='addclient'),
    path("clients/<int:client_id>/", ClientDetail.as_view(), name='detail_client'),
    path('clients/delete_comment/<int:pk>/', delete_comment, name='del')
]
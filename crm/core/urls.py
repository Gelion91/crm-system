from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='home'),
    path('addorder/', views.AddOrder.as_view(), name='addorder'),
    path('delete/<int:order_id>/', views.DeleteOrder.as_view(), name='delete'),
    path('addproduct/', views.AddProduct.as_view(), name='addproduct'),
    path('addclient/', views.AddClient.as_view(), name='addclient'),
    path('update/<int:order_id>/', views.update, name='upd'),
]

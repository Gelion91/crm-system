from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='home'),
    path('orders/active/', views.ActiveOrderListView.as_view(), name='active'),
    path('orders/on_pay/', views.WaitPayOrderListView.as_view(), name='on_pay'),
    path('orders/finish/', views.FinishOrderListView.as_view(), name='finish'),
    path('orders/addorder/', views.AddOrder.as_view(), name='addorder'),
    path('orders/delete/<int:order_id>/', views.DeleteOrder.as_view(), name='delete'),
    path('addproduct/', views.AddProduct.as_view(), name='addproduct'),
    path('orders/update/<int:order_id>/', views.update, name='upd'),
]

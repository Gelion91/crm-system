from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='home'),
    path('orders/all/', views.AllOrderListView.as_view(), name='all'),
    path('orders/on_pay/', views.WaitPayOrderListView.as_view(), name='on_pay'),
    path('orders/finish/', views.FinishOrderListView.as_view(), name='finish'),
    path('orders/addorder/', views.AddOrder.as_view(), name='addorder'),
    path('orders/delete/<int:order_id>/', views.DeleteOrder.as_view(), name='delete'),
    path('orders/updateproduct/<int:product_id>/', views.UpdateProduct.as_view(), name='upd_product'),
    path('orders/updateproduct/delete/<int:image_id>/', views.DeleteImage.as_view(), name='delete_image'),
    path('orders/update/<int:order_id>/', views.update, name='upd'),
    path('orders/update/delete/<int:product_id>/', views.DeleteProduct.as_view(), name='delete_product'),
    path('logistic/', views.DeliveryListView.as_view(), name='logistic'),
    path('logistic/sp', views.ProductStatus.as_view(), name='status_product'),
    path('logistic/status_delivery', views.DeliveryStatus.as_view(), name='status_delivery'),
    path('logistic/delete/<int:logistic_id>/', views.DeleteDelivery.as_view(), name='delete_logistic'),
    path('change_logistic_status', views.change_logistic_status, name='change_logistic_status'),
    path('change_status_paid', views.change_status_paid, name='change_status_paid'),
    path('change_status_arrive', views.change_status_arrive, name='change_status_arrive'),
    path('get_price', views.get_price, name='get_price'),
    path('save_image', views.save_image, name='save_image'),
    path('logistic/add_delivery', views.AddDelivery.as_view(), name='add_delivery'),
    path('logistic/update_delivery/<int:logistic_id>/', views.UpdateDelivery.as_view(), name='update_delivery'),
    path('account/add_acc/', views.AddAccount.as_view(), name='add_account'),
]

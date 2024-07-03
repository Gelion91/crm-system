from django.urls import path
from . import views

app_name = 'china'

urlpatterns = [
    path('logistic/', views.DeliveryStatus.as_view(), name='status_delivery'),
    path('logistic/sp', views.ProductStatus.as_view(), name='status_product'),
]

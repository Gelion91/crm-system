from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # path('', views.OrderChartView.as_view(), name='home'),
    path('', views.chart, name='home'),
]
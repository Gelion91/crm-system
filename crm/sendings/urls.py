from django.urls import path
from . import views

app_name = 'sendings'

urlpatterns = [
    path('', views.SendingsStatus.as_view(), name='sendings_list'),
    path('sending_create', views.SendingCreate.as_view(), name='sending_create'),
    path('sending_update/<int:sending_id>/', views.SendingUpdate.as_view(), name='sending_update'),
    path('sending_delete/<int:sending_id>/', views.SendingDelete.as_view(), name='sending_delete'),
    path('ajax_create_carrier', views.create_carrier, name='create_carrier'),
    path('ajax_save_notes_sending', views.save_notes_sending, name='save_notes_sending'),
    path('ajax_delete_notes_sending', views.delete_notes_sending, name='delete_notes_sending'),
    path('ajax_change_sending_status', views.change_sending_status, name='change_sending_status'),
    path('ajax_get_info', views.get_info, name='get_info'),
    path('ajax_show_logistic_info', views.show_logistic_info, name='show_logistic_info'),
    path('ajax_change_sending', views.change_sending, name='change_sending'),

]

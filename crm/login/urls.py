from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('registration', views.register, name='register'),
    path('update/<int:user_id>/', views.change_user_info, name='update_user')
]

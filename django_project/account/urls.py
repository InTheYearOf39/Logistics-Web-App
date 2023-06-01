from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register_package/', views.register_package, name='register_package'),
    path('recipient_dashboard/', views.recipient_dashboard, name='recipient_dashboard'),
    path('sender_dashboard/', views.sender_dashboard, name='sender_dashboard'),
    path('courier_dash/', views.courier_dashboard, name='courier_dash'),
    path('notification_count/', views.get_notification_count, name='notification_count'),
    path('completed_package/', views.completed_package, name='completed_package'),
]
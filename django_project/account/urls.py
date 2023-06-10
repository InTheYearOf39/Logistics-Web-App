from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.index, name='home'),
    path('base/', views.base, name='base'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout_user'),
    path('admin_dashboard/', views.admin, name='admin_dashboard'),
    path('sender_dashboard/', views.sender_dashboard, name='sender_dashboard'),
    path('register_package/', views.register_package, name='register_package'),
    path('recipient_dashboard/', views.recipient_dashboard, name='recipient_dashboard'),
    path('courier_dashboard/', views.courier_dashboard, name='courier_dashboard'),
    path('users/', views.users, name='users'),
    path('riders/', views.riders, name='riders'),
    path('admin_history/', views.admin_history, name='admin_history'),
    path('assign_courier/<int:package_id>/', views.assign_courier, name='assign_courier'),
    path('notify_arrival/<int:package_id>/', views.notify_arrival, name='notify_arrival'),
    path('confirm_delivery/<int:package_id>/',views.confirm_delivery, name='confirm_delivery'),
    path('sender_history/', views.sender_history, name='sender_history'),
    path('courier_history/', views.courier_history, name='courier_history'),
]
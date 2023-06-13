from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    site_views,
    sender_views,
    courier_views,
    admin_views,
    drop_pick_zone_views,
    authentication_views
)

urlpatterns = [

    # site routes
    path('', site_views.index, name='home'),
    path('services/', site_views.services, name='services'),
    path('about/', site_views.about, name='about'),
    path('contact/', site_views.contact, name='contact'),


    # authentication routes
    path('login/', authentication_views.login_view, name='login_view'),
    path('register/', authentication_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout_user'),


    # admin routes
    path('admin_dashboard/', admin_views.admin, name='admin_dashboard'),
    path('users/', admin_views.users, name='users'),
    path('riders/', admin_views.riders, name='riders'),
    path('admin_history/', admin_views.admin_history, name='admin_history'),
    path('assign_courier/<int:package_id>/', admin_views.assign_courier, name='assign_courier'),


    # sender routes
    path('sender_dashboard/', sender_views.sender_dashboard, name='sender_dashboard'),
    path('register_package/', sender_views.register_package, name='register_package'),
    path('sender_history/', sender_views.sender_history, name='sender_history'),


    # courier routes
    path('courier_dashboard/', courier_views.courier_dashboard, name='courier_dashboard'),
    path('notify_arrival/<int:package_id>/', courier_views.notify_arrival, name='notify_arrival'),
    path('confirm_delivery/<int:package_id>/', courier_views.confirm_delivery, name='confirm_delivery'),
    path('courier_history/', courier_views.courier_history, name='courier_history'),

    # Drop off and Pick up routes
    path('drop_pick_zone_dashboard/', drop_pick_zone_views.drop_pick_zone_dashboard, name='drop_pick_zone_dashboard'),
    path('confirm-drop-off/<int:package_id>/', drop_pick_zone_views.confirm_drop_off, name='confirm_drop_off'),
]
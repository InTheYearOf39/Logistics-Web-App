from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    site_views,
    sender_views,
    courier_views,
    admin_views,
    warehouse_views,
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
    path('change_password/', authentication_views.change_password, name='change_password'),


    # admin routes
    path('admin_dashboard/', admin_views.admin, name='admin_dashboard'),
    path('users/', admin_views.users, name='users'),
    path('riders/', admin_views.riders, name='riders'),
    path('admin_history/', admin_views.admin_history, name='admin_history'),
    path('admin_dashboard/assign_courier/<int:package_id>/', admin_views.assign_courier, name='admin_assign_courier'),
    path('dropoffs/', admin_views.dropoffs, name='dropoffs'),
    path('admin_dispatch/', admin_views.dispatch, name='admin_dispatch'),
    path('create_warehouse/', admin_views.create_warehouse, name='create_warehouse'),
    path('create_drop_pick/', admin_views.create_drop_pick, name='create_drop_pick'),
    path('warehouses/', admin_views.warehouses, name='warehouses'),
    path('drop_pick_zones/', admin_views.drop_pick_zones, name='drop_pick_zones'),


    # sender routes
    path('sender_dashboard/', sender_views.sender_dashboard, name='sender_dashboard'),
    path('register_package/', sender_views.register_package, name='register_package'),
    path('sender_history/', sender_views.sender_history, name='sender_history'),


    # courier routes
    path('courier_dashboard/', courier_views.courier_dashboard, name='courier_dashboard'),
    path('notify_arrival/<int:package_id>/', courier_views.notify_arrival, name='notify_arrival'),
    path('confirm_delivery/<int:package_id>/', courier_views.confirm_delivery, name='confirm_delivery'),
    path('courier_history/', courier_views.courier_history, name='courier_history'),


    # Warehouse routes
    path('warehouse_dashboard/', warehouse_views.warehouse_dashboard, name='warehouse_dashboard'),
    path('confirm_arrival/<int:package_id>/', warehouse_views.confirm_arrival, name='confirm_arrival'),
    path('ready_packages/', warehouse_views.ready_packages, name='ready_packages'),
    # path('reassign_courier/<int:package_id>/', warehouse_views.reassign_courier, name='reassign_courier'),

    # Drop off and Pick up routes
    path('drop_pick_zone_dashboard/', drop_pick_zone_views.drop_pick_zone_dashboard, name='drop_pick_zone_dashboard'),
    path('confirm-drop-off/<int:package_id>/', drop_pick_zone_views.confirm_drop_off, name='confirm_drop_off'),
    path('drop_pick_zone_dispatch/', drop_pick_zone_views.dispatch, name='dpz_dispatch'),
    path('dispatched_packages/', drop_pick_zone_views.dispatched_packages, name='dispatched_packages'),
    path('confirm_pickup/<int:package_id>/', drop_pick_zone_views.confirm_pickup, name='confirm_pickup'),

]
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
    path('home/', site_views.home, name='dashboard_home'),
    path('home_register/', site_views.home_register, name='home_register'),
    path('master_dashboard/', site_views.master_dashboard, name='master_dashboard'),


    # authentication routes
    path('login/', authentication_views.login_view, name='login_view'),
    path('register/', authentication_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout_user'),
    path('change_password/', authentication_views.change_password, name='change_password'),
	path('email-verification-sent/', authentication_views.email_verification_sent, name='email_verification_sent'),
    path('email-verification-failed/', authentication_views.email_verification_failed, name='email_verification_failed'),
    path('verify-email/', authentication_views.verify_email, name='verify_email'),

    # reset password routes
    path( 'reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form_.html"), 
        name= "reset_password"),
    path( 'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done_.html"), 
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm_.html"), 
        name="password_reset_confirm"),
    path( 'reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete_.html"), 
        name ="password_reset_complete"),


    # admin routes
    path('admin_dashboard/', admin_views.admin, name='admin_dashboard'),
    path('users/', admin_views.users, name='users'),
    path('riders/', admin_views.riders, name='riders'),
    path('warehouse_users/', admin_views.warehouse_users, name='warehouse_users'),
    path('drop_pick_users/', admin_views.drop_pick_users, name='drop_pick_users'),
    path('admin_history/', admin_views.admin_history, name='admin_history'),
    path('admin_dashboard/assign_courier/<int:package_id>/', admin_views.assign_courier, name='admin_assign_courier'),
    path('dropoffs/', admin_views.dropoffs, name='dropoffs'),
    path('admin_dispatch/', admin_views.dispatch, name='admin_dispatch'),
    path('create_warehouse/', admin_views.create_warehouse, name='create_warehouse'),
    path('create_warehouse_user/', admin_views.create_warehouse_user, name='create_warehouse_user'),
    path('create_drop_pick/', admin_views.create_drop_pick, name='create_drop_pick'),
    path('create_drop_pick_user/', admin_views.create_drop_pick_user, name='create_drop_pick_user'),
    path('create_courier/', admin_views.create_courier, name='create_courier'),
    path('warehouses/', admin_views.warehouses, name='warehouses'),
    path('edit_warehouse/<int:warehouse_id>/', admin_views.edit_warehouse, name='edit_warehouse'),
    path('delete_warehouse/<int:warehouse_id>/', admin_views.delete_warehouse, name='delete_warehouse'),
    path('edit_warehouse_user/<int:user_id>/', admin_views.edit_warehouse_user, name='edit_warehouse_user'),
    path('delete_warehouse_user/<int:user_id>/', admin_views.delete_warehouse_user, name='delete_warehouse_user'),
    path('drop_pick_zones/', admin_views.drop_pick_zones, name='drop_pick_zones'),
    path('edit_drop_pick_zones/<int:drop_pick_zone_id>/', admin_views.edit_drop_pick_zones, name='edit_drop_pick_zones'),
    path('delete_drop_pick_zone/<int:drop_pick_zone_id>/', admin_views.delete_drop_pick_zone, name='delete_drop_pick_zone'),
    # path('edit_drop_pick_zones/<int:drop_pick_zone_id>/', views.edit_drop_pick_zones, name='edit_drop_pick_zones'),
    path('edit_drop_pick_zone_user/<int:drop_pick_zone_user_id>/', admin_views.edit_drop_pick_zone_user, name='edit_drop_pick_zone_user'),
    path('delete_drop_pick_zone_user/<int:drop_pick_zone_user_id>/', admin_views.delete_drop_pick_zone_user, name='delete_drop_pick_zone_user'),



    # sender routes
    path('sender/dashboard/', sender_views.sender_dashboard, name='sender_dashboard'),
    path('register_package/', sender_views.register_package, name='register_package'),
    path('api/', sender_views.api, name='api'),
    path('sender_history/', sender_views.sender_history, name='sender_history'),


    # courier routes
    path('courier/dashboard/', courier_views.courier_dashboard, name='courier_dashboard'),
    path('notify_arrival/<int:package_id>/', courier_views.notify_arrival, name='notify_arrival'),
    path('notify_recipient/<int:package_id>/', courier_views.notify_recipient, name='notify_recipient'),
    path('confirm_delivery/<int:package_id>/', courier_views.confirm_delivery, name='confirm_delivery'),
    path('courier_history/', courier_views.courier_history, name='courier_history'),
    path('notify_dropoff/<int:package_id>/', courier_views.notify_dropoff, name='notify_dropoff'),


    # Warehouse routes
    path('warehouse/dashboard/', warehouse_views.warehouse_dashboard, name='warehouse_dashboard'),
    path('confirm_arrival/<int:package_id>/', warehouse_views.confirm_arrival, name='confirm_arrival'),
    path('new_arrivals/', warehouse_views.new_arrivals, name='new_arrivals'),
    path('ready_packages/', warehouse_views.in_house, name='in_house'),
    path('ready_for_pickup/', warehouse_views.ready_for_pickup, name='ready_for_pickup'),
    path('to_pickup/<int:package_id>/', warehouse_views.to_pickup, name='to_pickup'),
    # path('reassign_courier/<int:package_id>/', warehouse_views.reassign_courier, name='reassign_courier'),


    # Drop off and Pick up routes
    path('drop_pick_zone/dashboard/', drop_pick_zone_views.drop_pick_zone_dashboard, name='drop_pick_zone_dashboard'),
    path('confirm-drop-off/<int:package_id>/', drop_pick_zone_views.confirm_drop_off, name='confirm_drop_off'),
    path('drop_pick_zone/received/', drop_pick_zone_views.received_packages, name='received_packages'),
    path('dispatched_packages/', drop_pick_zone_views.dispatched_packages, name='dispatched_packages'),
    path('confirm_pickup/<int:package_id>/', drop_pick_zone_views.confirm_pickup, name='confirm_pickup'),
    path('confirm_at_pickup/<int:package_id>/', drop_pick_zone_views.confirm_at_pickup, name='confirm_at_pickup'),
    path('confirm_recipient_pickup/<int:package_id>/', drop_pick_zone_views.confirm_recipient_pickup, name='confirm_recipient_pickup'),
    # path('delivery_courier/<int:package_id>/', drop_pick_zone_views.delivery_courier, name='delivery_courier'),
    path('confirm_pickedup/<int:package_id>/', drop_pick_zone_views.confirm_pickedup, name='confirm_pickedup'),
    
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout_user'),
    path('register_package/', views.register_package, name='register_package'),
    path('recipient_dashboard/', views.recipient_dashboard, name='recipient_dashboard'),
    path('courier_dash/', views.courier_dash, name='courier_dash'),
    path('completed_pack/', views.completed_pack, name='completed_pack'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_management/', views.user_management, name='user_management'),
    path('create_user/', views.create_user,  name='create_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('view_packages/', views.view_packages, name='view_packages'),
    path('couriers/', views.couriers, name='couriers'),

]
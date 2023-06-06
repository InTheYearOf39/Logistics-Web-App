from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import assign_courier

urlpatterns = [

    path('admin_dashboard/', views.admin, name='admin_dashboard'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout_user'),
    path('register_package/', views.register_package, name='register_package'),
    path('recipient_dashboard/', views.recipient_dashboard, name='recipient_dashboard'),
    path('courier_dashboard/', views.courier_dashboard, name='courier_dashboard'),
    path('users/', views.users, name='users'),
    path('riders/', views.riders, name='riders'),
    path('assign_courier/<int:package_id>/', assign_courier, name='assign_courier'),
]
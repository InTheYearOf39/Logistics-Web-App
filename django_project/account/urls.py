from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout_user'),
    path('register_package/', views.register_package, name='register_package'),
]
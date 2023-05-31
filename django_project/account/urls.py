from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('recipient_dashboard/', views.recipient_dashboard, name='recipient_dashboard'),
]
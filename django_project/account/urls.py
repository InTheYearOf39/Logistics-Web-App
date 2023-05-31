from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('senderpage/', views.sender, name='senderpage'),
    path('receiverpage/', views.receiver, name='receiverpage'),
    path('courrierpage/', views.courrier, name='courrierpage'),
]
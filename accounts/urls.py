# coding=utf-8

from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('perfil/', views.profile, name='profile'),
    path('alterar-senha', views.update_password, name='update_password'),
]
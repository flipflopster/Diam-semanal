from django.contrib import admin
from django.urls import path

from . import views

app_name = 'gameapp'


urlpatterns = [
    path("", views.index, name='index'),

    path("login", views.login_page, name='login'),
    path("", views.login_load, name='login_load'),
    path("signin", views.signin_page, name='signin'),
    path("", views.signin_load, name='signin_load'),

    path("profile", views.profile_page, name='profile'),
]
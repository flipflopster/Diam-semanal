from django.contrib import admin
from django.urls import path

from . import views

app_name = ('gameapp')


urlpatterns = [
    path("", views.index, name='index'),

    path("login", views.login_page, name='login'),
    path("login/load", views.login_load, name='login_load'),
    path("signin", views.signin_page, name='signin'),
    path("signin/load", views.signin_load, name='signin_load'),

    path("profile", views.profile_page, name='profile'),
    path("logout", views.logout_load, name='logout'),


    path("searchResults", views.search_results, name='searchResults'),
    path("gameAddedToList", views.gameAddedToList, name='gameAddedToList'),
    path("<int:appId>/gameDetails", views.gameDetails, name='gameDetails'),
    path("<int:appId>/addTolist", views.addToList, name='addToList'),
    path("<int:appId>/threadsForGameSearch", views.threadsForGameSearch, name='threadsForGameSearch'),
]

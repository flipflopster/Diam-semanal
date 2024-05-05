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

    path("profileEdit", views.profileEdit, name='profileEdit'),
    path("<int:userId>/profileView", views.profileView, name='profileView'),
    path("logout", views.logout_load, name='logout'),


    path("searchResults", views.search_results, name='searchResults'),
    path("gameAddedToList", views.gameAddedToList, name='gameAddedToList'),
    path("<int:appId>/gameDetailsView", views.gameDetailsView, name='gameDetailsView'),
    path("<int:appId>/addTolist", views.addToList, name='addToList'),
    path("<int:appId>/threadsForGameSearch", views.threadsForGameSearch, name='threadsForGameSearch'),
    path("<int:appId>/createThread", views.createThread, name='createThread'),
    path("submitThread", views.submitThread, name='submitThread'),
    path("threadView/<int:threadId>",views.threadView, name='threadView'),
    path("<int:threadId>/createComment", views.createComment, name='createComment'),
    path("submitComment", views.submitComment, name='submitComment'),
    path("addFriend/<int:userId>", views.addFriend, name='addFriend'),
    path("removeFriend/<int:userId>", views.removeFriend, name='removeFriend'),
    path("topGamesResults", views.topGamesResults, name='topGamesResults'),
    path("popularGamesResults", views.popularGamesResults, name='popularGamesResults'),
    path("<int:appId>/gameRemovedFromList", views.gameRemovedFromList, name='gameRemovedFromList'),
    path("recentThreadsResults", views.recentThreadsResults, name='recentThreadsResults'),
    path("<int:appId>/createReview", views.createReview, name='createReview'),
    path("<int:userId>/userListView", views.userListView, name='userListView'),
    path("submitReview", views.submitReview, name='submitReview'),

]

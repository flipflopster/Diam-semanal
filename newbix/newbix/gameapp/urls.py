from django.contrib import admin
from django.urls import path

from . import views

app_name = ('gameapp')


urlpatterns = [
    path("", views.index, name='index'),

    # User Urls
    path("login", views.login_page, name='login'),
    path("login/load", views.login_load, name='login_load'),
    path("signin", views.signin_page, name='signin'),
    path("signin/load", views.signin_load, name='signin_load'),
    path("logout", views.logout_load, name='logout'),

    # Profile Urls
    path("update", views.update_profile, name='update'),
    path("settings", views.profile_settings, name='settings'),
    path("profile/<int:userId>", views.profile_page, name='profile_page'),
    path("addFriend/<int:userId>", views.addFriend, name='addFriend'),
    path("removeFriend/<int:userId>", views.removeFriend, name='removeFriend'),

    # Games Search and List Urls
    path("searchResults", views.search_results, name='searchResults'),
    path("<int:appId>/gameDetailsView", views.gameDetailsView, name='gameDetailsView'),
    path("topGamesResults", views.topGamesResults, name='topGamesResults'),
    path("popularGamesResults", views.popularGamesResults, name='popularGamesResults'),
    path("gameAddedToList", views.gameAddedToList, name='gameAddedToList'),
    path("<int:appId>/gameRemovedFromList", views.gameRemovedFromList, name='gameRemovedFromList'),

    # Thread Urls
    path("<int:appId>/threadsForGameSearch", views.threadsForGameSearch, name='threadsForGameSearch'),
    path("<int:appId>/createThread", views.createThread, name='createThread'),
    path("submitThread", views.submitThread, name='submitThread'),
    path("threadView/<int:threadId>", views.threadView, name='threadView'),
    path("recentThreadsResults", views.recentThreadsResults, name='recentThreadsResults'),
    path("threadList/<int:userId>", views.userThreadResults, name='userThreads'),

    path("<int:threadId>/createComment", views.createComment, name='createComment'),
    path("submitComment", views.submitComment, name='submitComment'),

    path("<int:appId>/createReview", views.createReview, name='createReview'),
    path("<int:userId>/userListView", views.userListView, name='userListView'),
    path("submitReview", views.submitReview, name='submitReview'),
    path("<int:appId>/reviewsForGameSearch", views.reviewsForGameSearch, name='reviewsForGameSearch'),
    path("reviewView/<int:reviewId>", views.reviewView, name='reviewView'),
    path("recentReviewsResults", views.recentReviewsResults, name='recentReviewsResults'),
    path("reviewList/<int:userId>", views.userReviewsResults, name='userReviews'),

    path("<int:appId>/createGameplay", views.createGameplay, name='createGameplay'),
    path("submitGameplay", views.submitGameplay, name='submitGameplay'),
    path("<int:appId>/gameplaysForGameSearch", views.gameplaysForGameSearch, name='gameplaysForGameSearch'),
    path("gameplayView/<int:gameplayId>", views.gameplayView, name='gameplayView'),
    path("recentGameplays", views.recentGameplayResults, name='recentGameplays'),
    path("gameplayList/<int:userId>", views.userGameplayResults, name='userGameplays'),
    path("<int:commentId>/deleteComment", views.deleteComment, name='deleteComment'),
    path("<int:gameplayId>/deleteGameplay", views.deleteGameplay, name='deleteGameplay'),
    path("<int:threadId>/deleteThread", views.deleteThread, name='deleteThread'),


]

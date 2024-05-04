import django.contrib.auth.models
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django import forms
from .models import Utilizador, Thread
from .steamDataFetcher import get_search_results_array, get_game_details, cache_game_details, is_cached
from .models import ListaUtilizadorJogo
from .models import Jogo


def not_authenticated(user):
    return not user.is_authenticated


def index(request):
    return render(request, 'gameapp/index.html')

def threadsForGameSearch(request,appId):
    resultArrayThreads = Thread.objects.filter(jogo_id=appId)
    return render(request, 'gameapp/threadsForGameSearch.html', {'resultArrayThreads':resultArrayThreads, 'appId':appId})

def search_results(request):
    filter = request.POST['filter']
    searchKeyword = request.POST['search']
    print(filter)
    print(searchKeyword)
    resultArrayGames = ['empty']
    resultArrayUsers =['empty']
    resultArrayThreads = ['empty']
    if filter == 'games':
        resultArrayGames = get_search_results_array(searchKeyword)
    elif filter == 'threads':
        resultArrayThreads = Thread.objects.filter(titulo__icontains=searchKeyword)
    elif filter == 'users':
        resultArrayUsers = Utilizador.objects.filter(username__icontains=searchKeyword)
    elif filter == 'all':
        resultArrayGames = get_search_results_array(searchKeyword)
        resultArrayThreads = list(Thread.objects.filter(titulo__icontains=searchKeyword))
        resultArrayUsers = list(Utilizador.objects.filter(username__icontains=searchKeyword))

    for result in resultArrayGames:
        print(result)
    for result in resultArrayThreads:
        print(result)
    for result in resultArrayUsers:
        print(result)

    return render(request, 'gameapp/searchResults.html', {'keyword': searchKeyword, 'resultArrayGames':resultArrayGames, 'resultArrayThreads':resultArrayThreads, 'resultArrayUsers':resultArrayUsers, 'filter':filter,})

def gameDetails(request,appId):
    try:
        jogo = Jogo.objects.get(steam_id=appId)
        numeroRatings = jogo.numeroRatings
        totalPontos = jogo.totalPontos

    except Jogo.DoesNotExist:
        numeroRatings = 0
        totalPontos = 0

    if numeroRatings == 0:
        media = 0
    else:
        media = round(float(totalPontos / numeroRatings), 2)

    game_details = get_game_details(appId)
    request.session['game_details'] = game_details

    if request.user.is_authenticated:
        # Get the Utilizador object related to the User
        utilizador = Utilizador.objects.get(user_id=request.user)

        # Check if a ListaUtilizadorJogo record exists for the current user and game
        inList = ListaUtilizadorJogo.objects.filter(jogo_id=jogo, utilizador_id=utilizador).exists()
    else:
        inList = False

    return render(request, 'gameapp/gameDetails.html', {'game_details': game_details, 'numeroRatings':numeroRatings, 'media':media, 'inList':inList})

def addToList(request,appId):
    game_details = request.session.get('game_details', None)

    class GameForm(forms.Form):
        RATING_CHOICES = [(i, str(i)) for i in range(11)]
        STATUS_CHOICES = [
            (ListaUtilizadorJogo.EstadosJogo.COMPLETED, 'Completed'),
            (ListaUtilizadorJogo.EstadosJogo.PLANTOPLAY, 'Plan To Play'),
            (ListaUtilizadorJogo.EstadosJogo.DROPPED, 'Dropped'),
            (ListaUtilizadorJogo.EstadosJogo.PLAYING, 'Playing'),
            (ListaUtilizadorJogo.EstadosJogo.ONHOLD, 'On Hold')
        ]

        rating = forms.ChoiceField(choices=RATING_CHOICES)
        estado = forms.ChoiceField(choices=STATUS_CHOICES)

    form = GameForm()
    request.session['game_details'] = game_details
    return render(request, 'gameapp/addToList.html', {'game_details': game_details,'form':form,})

def gameAddedToList(request):
    game_details = request.session.get('game_details', None)
    new_rating = int(request.POST.get('rating'))  # replace with the actual rating from the form
    estado = request.POST.get('estado')  # replace status with estado


    cache_game_details(game_details.get('steam_appid'))


    try:
        jogo = Jogo.objects.get(steam_id=game_details.get('steam_appid'))

    except Jogo.DoesNotExist:
        # If no Jogo object with the given steam_id exists, create one
        jogo = Jogo.objects.create(
            steam_id=game_details.get('steam_appid'),
            nome=game_details.get('name'),
            numeroRatings=0,
            totalPontos=0
        )

    # Get the Utilizador object related to the User
    utilizador = Utilizador.objects.get(user_id=request.user)

    lista_utilizador_jogo, created = ListaUtilizadorJogo.objects.get_or_create(
        jogo_id=jogo,
        utilizador_id=utilizador,  # use the Utilizador object
        defaults={
            'estado': estado,  # replace status with estado
            'rating': new_rating  # replace with the actual rating from the form
        }
    )

    if created:
        # If the ListaUtilizadorJogo object is newly created, increment numeroRatings
        jogo.numeroRatings += 1
        jogo.totalPontos += new_rating
        jogo.save()

    else:
        # If the ListaUtilizadorJogo object already exists and the form data is different, update it
        if lista_utilizador_jogo.estado != estado or lista_utilizador_jogo.rating != new_rating:
            # Subtract the existing rating from totalPontos and add the new rating
            jogo.totalPontos -= lista_utilizador_jogo.rating
            jogo.totalPontos += new_rating
            jogo.numeroRatings = ListaUtilizadorJogo.objects.filter(jogo_id=jogo).count()
            jogo.save()

            # Update the estado and rating in the ListaUtilizadorJogo record
            lista_utilizador_jogo.estado = estado
            lista_utilizador_jogo.rating = new_rating
            lista_utilizador_jogo.save()

    request.session['game_details'] = game_details
    return gameDetails(request, game_details.get('steam_appid'))


@user_passes_test(not_authenticated, login_url='/gameapp/profile')
def login_page(request):
    return render(request, 'gameapp/login_page.html')


@user_passes_test(not_authenticated, login_url='/gameapp/profile')
def login_load(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('gameapp:index'))
    else:
        return render(request, 'gameapp/login_page.html', {'error_message': "Nome ou Password errados."})


@user_passes_test(not_authenticated, login_url='/gameapp/profile')
def signin_page(request):
    return render(request, 'gameapp/signin_page.html')


@user_passes_test(not_authenticated, login_url='/gameapp/profile')
def signin_load(request):
    username = request.POST['username']
    try:
        if User.objects.get(username=username):
            return render(request, 'gameapp/signin_page.html', {'error_message': "User already exists."})
    except django.contrib.auth.models.User.DoesNotExist:
        _ = None
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(username=username, email=email, password=password)
    Utilizador.objects.create(user_id=user)
    login(request, user)
    return index(request)


@login_required(login_url='/gameapp/login')
def profile_page(request):
    return render(request, 'gameapp/profile_page.html')


def logout_load(request):
    logout(request)
    return HttpResponseRedirect(reverse('gameapp:index'))

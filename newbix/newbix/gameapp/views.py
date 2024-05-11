import os
import random

import django.contrib.auth.models
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import FloatField, F
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django import forms
from .models import Utilizador, Thread, Comentario, Lista_Amigos, Review, has_review, ListaGameplays, Gameplay
from .steamDataFetcher import get_search_results_array, get_game_details, cache_game_details, is_cached, get_name, \
    get_background
from .models import ListaUtilizadorJogo
from .models import Jogo


def not_authenticated(user):
    return not user.is_authenticated


def index(request):
    return render(request, 'gameapp/index.html')


def threadsForGameSearch(request, appId):
    if not Jogo.objects.filter(steam_id=appId).exists():
        resultArrayThreads = []
        return render(request, 'gameapp/searchResults.html',
                      {'keyword': get_name(appId), 'resultArrayThreads': resultArrayThreads, 'filter': 'threads', })
    else:
        jogo = Jogo.objects.get(steam_id=appId)

    resultArrayThreads = Thread.objects.filter(jogo_id=jogo)

    return render(request, 'gameapp/searchResults.html',
                  {'keyword': jogo.nome, 'resultArrayThreads': resultArrayThreads, 'filter': 'threads', })


def gameplaysForGameSearch(request, appId):
    if not Jogo.objects.filter(steam_id=appId).exists():
        listaGameplaysAux = []
        return render(request, 'gameapp/searchResults.html',{'keyword': get_name(appId), 'resultArrayGameplays': listaGameplaysAux, 'filter': 'gameplays', })
    else:
        jogo = Jogo.objects.get(steam_id=appId)

    listaGameplaysAux = ListaGameplays.objects.filter(listaUtliziadorJogo_id__jogo_id=jogo)
    print(listaGameplaysAux)
    return render(request, 'gameapp/searchResults.html',{'keyword': jogo.nome, 'resultArrayGameplays': listaGameplaysAux, 'filter': 'gameplays', })


def reviewsForGameSearch(request, appId):
    if not Jogo.objects.filter(steam_id=appId).exists():
        resultArrayReviews = []
        render(request, 'gameapp/searchResults.html.html',
               {'resultArrayReviews': resultArrayReviews, 'keyword': get_name(appId), 'filter': 'reviews'})
    else:
        jogo = Jogo.objects.get(steam_id=appId)

    resultArrayReviews = list(Review.objects.filter(listaUtliziadorJogo_id__jogo_id=jogo))
    return render(request, 'gameapp/searchResults.html',
                  {'resultArrayReviews': resultArrayReviews, 'keyword': jogo.nome, 'filter': 'reviews'})


def reviewView(request, reviewId):
    review = Review.objects.get(id=reviewId)
    print(review.listaUtliziadorJogo_id.utilizador_id.username)

    return render(request, 'gameapp/reviewView.html',
                  {'review': review, 'steam_id': review.listaUtliziadorJogo_id.jogo_id.steam_id})

def gameplayView(request, gameplayId):
    gameplay = Gameplay.objects.get(id=gameplayId)
    gameplaylist = ListaGameplays.objects.get(gameplay_id=gameplay)

    return render(request, 'gameapp/gameplayView.html',
                  {'gameplaylist': gameplaylist, 'steam_id': gameplaylist.listaUtliziadorJogo_id.jogo_id.steam_id})


def threadView(request, threadId):
    thread = Thread.objects.get(id=threadId)
    commentArray = list(Comentario.objects.filter(thread_id=thread))
    jogo = thread.jogo_id

    if request.user.is_authenticated:
        # Get the Utilizador object related to the User
        utilizador = Utilizador.objects.get(user_id=request.user)

        # Check if a ListaUtilizadorJogo record exists for the current user and game
        if jogo:  # Only execute this line if jogo is not None
            inList = ListaUtilizadorJogo.objects.filter(jogo_id=jogo, utilizador_id=utilizador).exists()
        else:
            inList = False
    else:
        inList = False
    return render(request, 'gameapp/threadView.html',
                  {'thread': thread, 'commentArray': commentArray, 'inList': inList})


def search_results(request):
    filter = request.POST['filter']
    searchKeyword = request.POST['search']
    resultArrayGames, resultArrayUsers, resultArrayThreads, gamesArray = [], [], [], []
    match filter:
        case 'games':
            gamesArray = get_search_results_array(searchKeyword)
            for game in gamesArray:
                if get_game_details(game.get('id')[0]).get('type') == 'game':
                    resultArrayGames.append(get_game_details(game.get('id')[0]))
        case 'users':
            resultArrayUsers = Utilizador.objects.filter(username__icontains=searchKeyword)
        case 'threads':
            resultArrayThreads = Thread.objects.filter(titulo__icontains=searchKeyword)
        case 'all':
            gamesArray = get_search_results_array(searchKeyword)
            for game in gamesArray:
                if get_game_details(game.get('id')[0]).get('type') == 'game':
                    resultArrayGames.append(get_game_details(game.get('id')[0]))
            resultArrayThreads = list(Thread.objects.filter(titulo__icontains=searchKeyword))
            resultArrayUsers = list(Utilizador.objects.filter(username__icontains=searchKeyword))
    print(resultArrayGames, resultArrayUsers)
    return render(request, 'gameapp/searchResults.html',
                  {'keyword': searchKeyword, 'resultArrayGames': resultArrayGames,
                   'resultArrayThreads': resultArrayThreads, 'resultArrayUsers': resultArrayUsers, 'filter': filter, })


@login_required(login_url='/gameapp/login')
def createReview(request, appId):
    request.session['appId'] = appId
    game = Jogo.objects.get(steam_id=appId)
    review = request.user.utilizador.get_review(game)
    return render(request, 'gameapp/createReview.html', {'game': game, 'review': review})


@login_required(login_url='/gameapp/login')
def submitReview(request):
    appId = request.session.get('appId')
    game = Jogo.objects.get(steam_id=appId)
    luj = ListaUtilizadorJogo.objects.get(jogo_id=Jogo.objects.get(steam_id=appId),
                                          utilizador_id=Utilizador.objects.get(user_id=request.user))

    tipo = request.POST.get('tipo')
    texto = request.POST.get('texto')

    review = request.user.utilizador.get_review(game)
    if review:
        review.tipoReview = tipo
        review.texto = texto
        review.save()
    else:
        Review.objects.create(tipoReview=tipo, texto=texto, listaUtliziadorJogo_id=luj)

    return redirect('gameapp:gameDetailsView', appId=appId)


def gameDetailsView(request, appId):
    try:
        jogo = Jogo.objects.get(steam_id=appId)
    except Jogo.DoesNotExist:
        jogo = None

    gameDetails = get_game_details(appId)
    request.session['gameDetails'] = gameDetails

    lista = None
    if request.user.is_authenticated:
        if jogo:
            lista = request.user.utilizador.is_on_List(jogo)

    review = None
    if lista:
        review = has_review(lista)

    bg = get_background(appId)
    context = {'jogo': jogo, 'gameDetails': gameDetails, 'lista': lista, 'review': review, 'background': bg}

    return render(request, 'gameapp/gameDetailsView.html', context)


def userListView(request, userId):
    utilizador = Utilizador.objects.get(user_id=userId)
    resultArrayEntries = ListaUtilizadorJogo.objects.filter(utilizador_id=utilizador)
    return render(request, 'gameapp/userListView.html',
                  {'utilizador': utilizador, 'resultArrayEntries': resultArrayEntries})


@login_required(login_url='/gameapp/login')
def createThread(request, appId):
    game = Jogo.objects.get(steam_id=appId)
    request.session['appId'] = appId
    return render(request, 'gameapp/createThread.html', {'game': game})


@login_required(login_url='/gameapp/login')
def createComment(request, threadId):
    request.session['threadId'] = threadId
    return render(request, 'gameapp/createComment.html')


@login_required(login_url='/gameapp/login')
def submitThread(request, thread):
    appId = request.session.get('appId')
    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    jogo = Jogo.objects.get(steam_id=appId)
    utilizador = Utilizador.objects.get(user_id=request.user)

    Thread.objects.create(titulo=titulo, descricao=descricao, jogo_id=jogo, criador_id=utilizador)
    return threadsForGameSearch(request, appId)


@login_required(login_url='/gameapp/login')
def submitComment(request):
    threadId = request.session.get('threadId')
    texto = request.POST.get('text')
    Comentario.objects.create(texto=texto, thread_id=Thread.objects.get(id=threadId),
                              poster_id=Utilizador.objects.get(user_id=request.user))

    return redirect('gameapp:threadView', threadId=threadId)

@login_required(login_url='/gameapp/login')
def createGameplay(request, appId):
    request.session['appId'] = appId
    game = Jogo.objects.get(steam_id=appId)

    listaUserJogo = ListaUtilizadorJogo.objects.get(jogo_id=game, utilizador_id=Utilizador.objects.get(user_id=request.user))
    numeroGameplays = ListaGameplays.objects.filter(listaUtliziadorJogo_id=listaUserJogo).count()

    return render(request, 'gameapp/createGameplay.html', {'game': game, 'numeroGameplays':numeroGameplays})



@login_required(login_url='/gameapp/login')
def submitGameplay(request):

    appId = request.session.get('appId')
    descricao = request.POST.get('descricao')
    link = request.POST.get('link')
    titulo = request.POST.get('titulo')
    gameplay = Gameplay.objects.create(titulo=titulo, descricao=descricao, link=link)
    listaGameplays = ListaGameplays.objects.create(gameplay_id=gameplay, listaUtliziadorJogo_id=ListaUtilizadorJogo.objects.get(jogo_id=Jogo.objects.get(steam_id=appId), utilizador_id=Utilizador.objects.get(user_id=request.user)))


    return redirect('gameapp:gameDetailsView', appId=appId)


def gameplayListView(request,gameplayId):
    gameplays = Gameplay.objects.all().order_by('-created_at')
    return render(request, 'gameapp/gameplayListView.html', {'gameplays': gameplays})


def topGamesResults(request):
    resultArrayGamesAux = Jogo.objects.all().order_by('-media')
    resultArrayGames = []
    for game in resultArrayGamesAux:
        resultArrayGames.append(get_game_details(game.steam_id))
    return render(request, 'gameapp/searchResults.html',
                  {'keyword': 'Top Games', 'resultArrayGames': resultArrayGames, 'filter': 'games', })


def recentThreadsResults(request):
    resultArrayThreads = Thread.objects.all().order_by('-created_at')
    return render(request, 'gameapp/searchResults.html',
                  {'keyword': 'Recent Threads', 'resultArrayThreads': resultArrayThreads, 'filter': 'threads', })


def recentReviewsResults(request):
    resultArrayReviews = Review.objects.all().order_by('-created_at')
    return render(request, 'gameapp/searchResults.html',
                  {'keyword': 'Recent', 'resultArrayReviews': resultArrayReviews, 'filter': 'reviews'})


def popularGamesResults(request):
    resultArrayGamesAux = Jogo.objects.all().order_by('-numeroRatings')
    resultArrayGames = []
    for game in resultArrayGamesAux:
        resultArrayGames.append(get_game_details(game.steam_id))
    return render(request, 'gameapp/searchResults.html',
                  {'keyword': 'Popular Games', 'resultArrayGames': resultArrayGames, 'filter': 'games', })


@login_required(login_url='/gameapp/login')
def gameAddedToList(request):
    gameDetails = request.session.get('gameDetails', None)
    new_rating = int(request.POST.get('rating'))  # replace with the actual rating from the form
    estado = request.POST.get('estado')  # replace status with estado

    try:
        jogo = Jogo.objects.get(steam_id=gameDetails.get('steam_appid'))

    except Jogo.DoesNotExist:
        # If no Jogo object with the given steam_id exists, create one
        jogo = Jogo.objects.create(
            steam_id=gameDetails.get('steam_appid'),
            nome=gameDetails.get('name'),
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
        if estado == 'CM':
            utilizador.jogos_completos += 1
            utilizador.save()
    else:
        if lista_utilizador_jogo.estado == 'CM':
            if estado != 'CM':
                utilizador.jogos_completos -= 1
                utilizador.save()
        else:
            if estado == 'CM':
                utilizador.jogos_completos += 1
                utilizador.save()

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

    request.session['gameDetails'] = gameDetails
    return gameDetailsView(request, gameDetails.get('steam_appid'))


@login_required(login_url='/gameapp/login')
def gameRemovedFromList(request, appId):
    jogo = Jogo.objects.get(steam_id=appId)
    utilizador = Utilizador.objects.get(user_id=request.user)

    lista_utilizador_jogo = ListaUtilizadorJogo.objects.get(jogo_id=jogo, utilizador_id=utilizador)
    if lista_utilizador_jogo.estado == 'CM':
        utilizador.jogos_completos -= 1
        utilizador.save()

    ratingToSubtract = lista_utilizador_jogo.rating
    lista_utilizador_jogo.delete()

    jogo.numeroRatings = ListaUtilizadorJogo.objects.filter(jogo_id=jogo).count()

    jogo.totalPontos -= ratingToSubtract
    jogo.save()

    return gameDetailsView(request, appId)


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
    Utilizador.objects.create(user_id=user, username=username)
    login(request, user)
    return index(request)


def profile_page(request, userId):
    utilizador = Utilizador.objects.get(id=userId)

    if request.user.is_authenticated:
        utilizador_logado = Utilizador.objects.get(user_id=request.user)
        isFriend = Lista_Amigos.objects.filter(utilizador_id=utilizador_logado,
                                               utilizador_seguido_id=utilizador).exists()
    else:
        isFriend = False
    listaAmigos = Lista_Amigos.objects.filter(utilizador_id=utilizador).order_by('data')[:5]
    listaJogos = ListaUtilizadorJogo.objects.filter(utilizador_id=utilizador).filter(estado='CM').order_by('-rating')[
                 :3]

    last_review = utilizador.last_review()

    return render(request, 'gameapp/profile_page.html',
                  {'utilizador': utilizador, 'isFriend': isFriend, 'friends': listaAmigos, 'games': listaJogos,
                   'last_review': last_review})


def addFriend(request, userId):
    utilizador = Utilizador.objects.get(user_id=request.user)
    utilizador_seguido = Utilizador.objects.get(id=userId)
    if not utilizador == utilizador_seguido:
        Lista_Amigos.objects.create(utilizador_id=utilizador, utilizador_seguido_id=utilizador_seguido)
    return redirect('gameapp:profile_page', userId=userId)


def removeFriend(request, userId):
    utilizador = Utilizador.objects.get(user_id=request.user)
    utilizador_seguido = Utilizador.objects.get(id=userId)
    if not utilizador == utilizador_seguido:
        Lista_Amigos.objects.filter(utilizador_id=utilizador, utilizador_seguido_id=utilizador_seguido).delete()

    return redirect('gameapp:profile_page', userId=userId)


@login_required(login_url='/gameapp/login')
def profile_settings(request):
    return render(request, 'gameapp/profile_settings.html')


@login_required(login_url='/gameapp/login')
def logout_load(request):
    logout(request)
    return HttpResponseRedirect(reverse('gameapp:index'))


@login_required(login_url='/gameapp/login')
def update_profile(request):
    utilizador = request.user.utilizador
    utilizador.biografia = request.POST['bio']
    utilizador.localidade = request.POST['local']
    utilizador.genero = request.POST['genero']
    context = {'update': 'Profile updated'}
    try:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        if utilizador.profile_picture:
            filename = utilizador.profile_picture
            fs.delete(filename.split("/")[1])
        filename = fs.save(myfile.name, myfile)
        utilizador.profile_picture = "media/" + filename
    except django.utils.datastructures.MultiValueDictKeyError:
        _ = None
    utilizador.save()
    return render(request, 'gameapp/profile_settings.html', context)

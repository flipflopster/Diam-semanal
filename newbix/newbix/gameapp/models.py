import datetime
import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from .steamDataFetcher import is_cached, cache_game_details, remove_from_cache, get_capsule_imagev5, get_screenshots, \
    get_header_img


def has_review(lista):
    try:
        review = Review.objects.get(listaUtilizadorJogo_id=lista)
    except Review.DoesNotExist:
        review = None
    return review


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)

    genero = models.CharField(max_length=50, default='Not Specified')
    biografia = models.CharField(max_length=255)
    localidade = models.CharField(max_length=100)
    jogos_completos = models.IntegerField(default=0)
    profile_picture = models.CharField(max_length=100)

    def get_review(self, jogo):
        lista = self.is_on_List(jogo)
        try:
            review = Review.objects.get(listaUtilizadorJogo_id=lista)
        except Review.DoesNotExist:
            review = None
        return review

    def last_review(self):
        r = None
        for game in ListaUtilizadorJogo.objects.filter(utilizador_id=self):
            review = Review.objects.filter(listaUtilizadorJogo_id=game).first()
            if review:
                if r:
                    if review.updated > r.updated:
                        r = review
                else:
                    r = review
        return r

    def is_on_List(self, jogo):
        try:
            lista = ListaUtilizadorJogo.objects.get(jogo_id=jogo, utilizador_id=self)
        except ListaUtilizadorJogo.DoesNotExist:
            lista = None
        return lista

    def count_completes(self):
        lista = ListaUtilizadorJogo.objects.filter(utilizador_id=self, estado='Completed')
        self.jogos_completos = lista.count()
        self.save()


class Lista_Amigos(models.Model):
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='utilizador_id')
    utilizador_seguido = models.ForeignKey(Utilizador, on_delete=models.CASCADE,
                                              related_name='utilizador_seguido_id')
    data = models.DateTimeField(auto_now_add=True)

    def nomes(self):
        def get_username_attributes(utilizador_id, utilizador_seguido_id):
            utilizador = Utilizador.objects.get(id=utilizador_id)
            utilizador_seguido = Utilizador.objects.get(id=utilizador_seguido_id)
            return utilizador.username, utilizador_seguido.username

        username1, username2 = get_username_attributes(self.utilizador_id, self.utilizador_seguido_id)

        return username1, username2


class Jogo(models.Model):
    nome = models.CharField(max_length=100)
    steam_id = models.IntegerField()
    totalPontos = models.IntegerField(default=0)
    numeroRatings = models.IntegerField(default=0)
    media = models.FloatField(default=0)

    def get_header(self):
        return get_header_img(self.steam_id)

    def get_img_url(self):
        return get_capsule_imagev5(self.steam_id)

    def get_background(self):
        sShots = get_screenshots(self.steam_id)
        background = None
        if sShots:
            background = random.choice(sShots)
        return background

    def save(self, *args, **kwargs):
        if not is_cached(self.steam_id):
            cache_game_details(self.steam_id)

        if self.numeroRatings != 0:
            self.media = round(float(self.totalPontos / self.numeroRatings), 2)
        else:
            self.media = 0
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        remove_from_cache(self.steam_id)

        # call the original delete method
        super(Jogo, self).delete(*args, **kwargs)

    def __str__(self):
        return self.nome

    def steamId(self):
        return self.steam_id

    def count_media(self):
        lista = ListaUtilizadorJogo.objects.filter(jogo_id=self)
        total = 0
        for rating in lista:
            total += rating.rating

        self.numeroRatings = lista.count()
        self.totalPontos = total
        self.save()


class ListaUtilizadorJogo(models.Model):
    class EstadosJogo(models.TextChoices):
        COMPLETED = 'CM', 'Completed'
        PLANTOPLAY = 'PP', 'Plan To Play'
        DROPPED = 'DR', 'Dropped'
        PLAYING = 'PL', 'Playing'
        ONHOLD = 'OH', 'On Hold'

    estado = models.CharField(
        max_length=2,
        choices=EstadosJogo.choices,
        default=EstadosJogo.PLANTOPLAY,
    )
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_altered = models.DateTimeField(auto_now=True)


class Review(models.Model):
    listaUtilizadorJogo = models.OneToOneField(ListaUtilizadorJogo, on_delete=models.CASCADE)
    texto = models.CharField(max_length=511)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class tipoReview(models.TextChoices):
        MIXED_FEELINGS = 'MF', 'Mixed Feelings'
        RECOMMENDED = 'RC', 'Recommended'
        NOT_RECOMMENDED = 'DR', 'Not Recommended'

    tipoReview = models.CharField(max_length=2, choices=tipoReview.choices)


class Gameplay(models.Model):
    titulo = models.CharField(max_length=127)
    descricao = models.CharField(max_length=255)
    link = models.CharField(max_length=127)
    created_at = models.DateTimeField(auto_now_add=True)


class LinksUtilizador(models.Model):
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    link = models.CharField(max_length=127)


class ListaGameplays(models.Model):
    listaUtilizadorJogo = models.ForeignKey(ListaUtilizadorJogo, on_delete=models.CASCADE)
    gameplay = models.ForeignKey(Gameplay, on_delete=models.CASCADE)



class ListaThreads(models.Model):
    listaUtilizadorJogo = models.OneToOneField(ListaUtilizadorJogo, on_delete=models.CASCADE)
    contagem = models.IntegerField(default=0)



class Thread(models.Model):
    listaThreads = models.ForeignKey(ListaThreads, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=127)
    descricao = models.CharField(max_length=511)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class threadTopic(models.TextChoices):
        GAME_BUILD = 'GB', 'Game Build'
        STRATEGY = 'SG', 'Strategy'
        COMPETITIVE = 'CP', 'Competitive'
        MODDING = 'MO', 'Modding'
        COMPLETION = 'CO', 'Completion'
        GAME_UPDATES = 'GU', 'Game Updates'
        GAME_EVENTS = 'GE', 'Game Events'
        LORE = 'LO', 'Lore'
        SOUNDTRACK = 'ST', 'Soundtrack'
        GRAPHICS = 'GR', 'Graphics'
        GAME_MECHANICS = 'GM', 'Game Mechanics'
        EASTER_EGGS = 'EE', 'Easter Eggs'
        OTHER = 'OT', 'Other'

    threadTopic = models.CharField(max_length=2, choices=threadTopic.choices, default=threadTopic.OTHER)


class Comentario(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

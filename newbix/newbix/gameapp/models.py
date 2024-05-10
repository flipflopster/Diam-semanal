import datetime
import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from .steamDataFetcher import is_cached, cache_game_details, remove_from_cache, get_capsule_imagev5, get_screenshots


# def loginview(request):
#    username = request.POST['username']
#    password = request.POST['password']
#    user = authenticate(username=username,
#                        password=password)
#    if user is not None:
#        login(request, user)
#    else:

class Utilizador(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)

    genero = models.CharField(max_length=50, default='Not Specified')
    biografia = models.CharField(max_length=255)
    localidade = models.CharField(max_length=100)
    jogos_completos = models.IntegerField(default=0)
    profile_picture = models.CharField(max_length=100)

    def last_review(self):
        r = None
        for game in ListaUtilizadorJogo.objects.filter(utilizador_id=self):
            review = Review.objects.filter(listaUtliziadorJogo_id=game).first()
            if review:
                if r:
                    if review.updated > r.updated:
                        r = review
                else:
                    r = review
        return r


class Lista_Amigos(models.Model):
    utilizador_id = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='utilizador_id')
    utilizador_seguido_id = models.ForeignKey(Utilizador, on_delete=models.CASCADE,
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
    utilizador_id = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    jogo_id = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_altered = models.DateTimeField(auto_now=True)


class Review(models.Model):
    listaUtliziadorJogo_id = models.OneToOneField(ListaUtilizadorJogo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=127)
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
    utilizador_id = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    link = models.CharField(max_length=127)


class ListaGameplays(models.Model):
    listaUtliziadorJogo_id = models.ForeignKey(ListaUtilizadorJogo, on_delete=models.CASCADE)
    gameplay_id = models.ForeignKey(Gameplay, on_delete=models.CASCADE)


class Thread(models.Model):
    criador_id = models.ForeignKey(Utilizador, on_delete=models.SET_NULL, null=True)
    jogo_id = models.ForeignKey(Jogo, on_delete=models.CASCADE)
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
    thread_id = models.ForeignKey(Thread, on_delete=models.CASCADE)
    poster_id = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


"""


class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)

class Personagem(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)


class ListaJogoPersonagem(models.Model):
    jogo_id = models.OneToManyField(Jogo, on_delete=models.CASCADE)
    personagem_id = models.OneToManyField(Pesonagem, on_delete=models.CASCADE)

class FotosJogo(models.Model):
    jogo_id = models.OneToManyField(Jogo, on_delete=models.CASCADE)
    fotoLink = models.CharField(max_length=255)

    class TiposImagens(models.TextChoices):
        THUMBNAIL = 'TN', _('Thumbnail')
        BANNER = 'BN', _('Banner')
        INGAME = 'IG', _('In Game')


    tipo = models.CharField(
        max_length=2,
        choices=TiposImagens.choices,
        default=TiposImagens.INGAME,
    )


    curso = models.CharField(max_length=100)
    votosmax = models.IntegerField()
    votos = models.IntegerField(default=0)
    profile_picture = models.CharField(max_length=100)

    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    opcao_texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.opcao_texto

    objects = None
    questao_texto = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.questao_texto

    def recente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)
"""

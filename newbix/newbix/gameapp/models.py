import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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

    genero = models.CharField(max_length=50)
    biografia = models.CharField(max_length=255)
    localidade = models.CharField(max_length=100)
    jogos_completos = models.IntegerField()
    profile_picture = models.CharField(max_length=100)


class Lista_Amigos(models.Model):
    utilizador_id = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='utilizador_id')
    utilizador_seguido_id = models.ForeignKey(Utilizador, on_delete=models.CASCADE,
                                              related_name='utilizador_seguido_id')

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

    def __str__(self):
        return self.nome

    def steamId(self):
        return self.steam_id

    def media(self):
        return round(float(self.totalPontos / self.numeroRatings), 2)


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


class Review(models.Model):
    listaUtliziadorJogo_id = models.OneToOneField(ListaUtilizadorJogo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=127)
    texto = models.CharField(max_length=511)


class Gameplay(models.Model):
    titulo = models.CharField(max_length=127)
    descricao = models.CharField(max_length=255)
    link = models.CharField(max_length=127)


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
    data = models.DateTimeField('data de publicacao')
    

class Comentario(models.Model):
    thread_id = models.ForeignKey(Thread, on_delete=models.CASCADE)
    poster_id = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    data = models.DateTimeField('data de publicacao')

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

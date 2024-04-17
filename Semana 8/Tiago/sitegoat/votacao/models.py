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

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)
    votosmax = models.IntegerField()
    votos = models.IntegerField(default=0)
    profile_picture = models.CharField(max_length=100)


class Questao(models.Model):
    objects = None
    questao_texto = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.questao_texto

    def recente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)


class Opcao(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    opcao_texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.opcao_texto

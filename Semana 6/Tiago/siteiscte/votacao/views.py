from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from .models import Questao, Opcao, Aluno

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# adicionar administrador esta autenticado no criarquestao,criaropcao, removerquestao e removeropcao


# Função para registar novo Utilizador
def registaruser(request):
    if request.method == 'POST':
        try:
            nameuser = request.POST.get('novouser')
            emailuser = request.POST.get('novouseremail')
            passworduser = request.POST.get('novouserpassword')
            cursouser = request.POST.get('novousercurso')
        except KeyError:
            return render(request, 'votacao/registar.html')

        user = User.objects.create_user(nameuser, emailuser, passworduser)
        user.save()
        Aluno(user=user, curso=cursouser, numvotos=0).save()
        return HttpResponseRedirect(reverse('votacao:loginview'))
    else:
        return render(request, 'votacao/registar.html')


# Função para obter os dados de um Utilizador
def perfil(request):
    return render(request, 'votacao/meu_perfil.html')


# Função para fazer o login
def loginview(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            return render(request, 'votacao/login.html')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('votacao:index'))
        # Criar mensagem de erro
    else:
        return render(request, 'votacao/login.html')


# Função para fazer o logout
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:loginview'))


def criarquestao(request):
    if request.method == 'POST':
        try:
            questao_texto = request.POST.get("novaquestao")
        except KeyError:
            return render(request, 'votacao/criarquestao.html')
        if questao_texto:
            if request.user.is_superuser:
                questao = Questao(questao_texto=questao_texto, pub_data=timezone.now())
                questao.save()
            return HttpResponseRedirect(reverse('votacao:index'))

            # adicionar messagem de erro a indicar que o utilizador não é o administrador
        else:
            return HttpResponseRedirect(reverse('votacao:criarquestao'))
    else:
        return render(request, 'votacao/criarquestao.html')


def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.method == 'POST':
        try:
            opcao = request.POST.get('adicionaropcao')
        except KeyError:
            return render(request, 'votacao/criarquestao.html', {'questao': questao})
        if opcao:
            if request.user.is_superuser:
                novaopcao = questao.opcao_set.create(opcao_texto=opcao, votos=0)
                novaopcao.save()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
            # adicionar messagem de erro a indicar que o utilizador não é o administrador
        else:
            return HttpResponseRedirect(reverse('votacao:criaropcao', args=(questao.id,)))
    else:
        return render(request, 'votacao/criaropcao.html', {'questao': questao})


def removerquestao(request, questao_id):
    if request.user.is_superuser:
        questao = get_object_or_404(Questao, pk=questao_id)
        if questao.opcao_set.count() > 0:
            for opcao in questao.opcao_set.all():
                opcao.delete()
        questao.delete()

    return HttpResponseRedirect(reverse('votacao:index'))


def removeropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        return render(request, 'votacao/detalhe.html', {
            'questao': questao,
            'error_message': "Não escolheu uma opção",
        })
    else:
        if request.user.is_superuser:
            opcao_seleccionada.delete()
    return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))


# Função para o Index
# criar condiçao para ser reencaminhado para o login
def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'votacao/index.html', context)


# Função para obter as opções de votos numa questão
def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


# Função para obter os número de cada voto numa questão após ser feita um novo voto
def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


# Função para obter adicionar um voto numa questão
def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {
            'questao': questao,
            'error_message': "Não escolheu uma opção",
        })
    else:
        if request.user.is_authenticated:
            if request.user.aluno.numvotos >= int(request.user.aluno.curso[-1]) + 5:
                return render(request, 'votacao/detalhe.html', {
                    'questao': questao,
                    'error_message': "Limite de votos excedido",
                })

            opcao_seleccionada.votos += 1
            opcao_seleccionada.save()
            request.user.aluno.numvotos += 1
            request.user.aluno.save()
        else:
            return render(request, 'votacao/detalhe.html', {
                'questao': questao,
                'error_message': "Utilizador não se encontra Autenticado",
            })

    return HttpResponseRedirect(
        reverse('votacao:resultados', args=(questao.id,)))

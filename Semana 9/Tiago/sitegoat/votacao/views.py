import django.contrib.auth.models
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Questao, Opcao, Aluno
from django.contrib.auth import authenticate, login, logout




def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)


def not_LogIn(user):
    return not user.is_authenticated


@user_passes_test(not_LogIn, login_url='/votacao/userPage')
def loginPage(request):
    return render(request, 'votacao/loginPage.html')


@user_passes_test(not_LogIn, login_url='/votacao/userPage')
def loadLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('votacao:index'))
    else:
        return render(request, 'votacao/loginPage.html', {'error_message': "Este utilizador não existe."})


@user_passes_test(not_LogIn, login_url='/votacao/userPage')
def registar(request):
    return render(request, 'votacao/registar.html')


@user_passes_test(not_LogIn, login_url='/votacao/userPage')
def loadRegistar(request):
    username = request.POST['username']
    try:
        if User.objects.get(username=username):
            return render(request, 'votacao/registar.html', {'error_message': "Este Utilizador já existe."})
    except django.contrib.auth.models.User.DoesNotExist:
        _ = None
    curso = request.POST['curso']
    try:
        aux = curso.split('-')[1].isdigit()
    except ValueError and IndexError:
        aux = False
    if not aux:
        return render(request, 'votacao/registar.html',
                      {'error_message': "Curso necessita estar no formato: (Nome)-(Número de Turma)."})
    else:
        nums = [*curso.split('-')[1]]
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, email=email, password=password)
        Aluno.objects.create(user=user, votosmax=int(nums[len(nums) - 1]) + 5)
        login(request, user)
        return index(request)


@login_required(login_url='/votacao/loginPage')
def userPage(request):
    return render(request, 'votacao/userPage.html')


@login_required(login_url='/votacao/loginPage')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:index'))


@login_required(login_url='/votacao/loginPage')
def trataropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {'questao': questao, 'error_message': "Não escolheu uma opção"})
    else:
        value = request.POST['value']
        if value == "Voto":
            user = request.user.aluno
            if user.votos != user.votosmax:
                user.votos += 1
                user.save()
                opcao_seleccionada.votos += 1
                opcao_seleccionada.save()
                context = {'questao': questao}
            else:
                context = {'questao': questao, 'error_message': "Não pode fazer mais votos."}
            return render(request, 'votacao/resultados.html', context)
        else:
            opcao_seleccionada.delete()
            return render(request, 'votacao/detalhe.html', {'questao': questao})


@login_required(login_url='/votacao/loginPage')
def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.user.is_authenticated:
        return render(request, 'votacao/detalhe.html', {'questao': questao})
    else:
        return render(request, 'votacao/resultados.html', {'questao': questao})


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


@login_required(login_url='/votacao/loginPage')
@permission_required("superuser", login_url='/votacao')
def criarquestao(request):
    return render(request, 'votacao/criarquestao.html')


@permission_required("superuser", login_url='/votacao')
def submeterquestao(request):
    questaotexto = request.POST.get('questaotexto')
    if questaotexto == '':
        return render(request, 'votacao/criarquestao.html', {'error_message': "Não escreveu nenhuma Questão."})
    else:
        q = Questao.objects.create(questao_texto=questaotexto, pub_data=timezone.now())
        q.save()
        return HttpResponseRedirect(reverse('votacao:index'))


@permission_required("superuser", login_url='/votacao')
def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/criaropcao.html', {'questao': questao})


@permission_required("superuser", login_url='/votacao')
def submeteropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    opcaotexto = request.POST.get('opcaotexto')
    if opcaotexto == '' or opcaotexto is None:
        return render(request, 'votacao/criaropcao.html',
                      {'questao': questao, 'error_message': "Não escreveu nenhuma Opção."})
    else:
        o = Opcao.objects.create(questao=questao, opcao_texto=opcaotexto, votos=0)
        o.save()
        return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))


@permission_required("superuser", login_url='/votacao')
def deletequestao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    questao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))


@permission_required("superuser", login_url='/votacao')
def deleteopcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {'questao': questao, 'error_message': "Não escolheu uma opção"})
    else:
        opcao.delete()
        opcao.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
    return render(request, 'votacao/detalhe.html', {'questao': questao})


@login_required(login_url='/votacao/loginPage')
def uploadpp(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        user = request.user.aluno
        if user.profile_picture:
            print("silly")
            filename = user.profile_picture
            fs.delete(filename.split("/")[1])
        filename = fs.save(myfile.name, myfile)
        user.profile_picture = "media/" + filename
        user.save()
        return render(request, 'votacao/userPage.html', {'uploaded_file_url': "media/" + filename})
    return render(request, 'votacao/userPage.html', {'error_message': "Não escolheu nenhum ficheiro."})

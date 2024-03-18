from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Questao, Opcao


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
            opcao_seleccionada.votos += 1
            opcao_seleccionada.save()
            return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))
        else:
            opcao_seleccionada.delete()
            return render(request, 'votacao/detalhe.html', {'questao': questao})


def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


def criarquestao(request):
    return render(request, 'votacao/criarquestao.html')


def submeterquestao(request):
    questaotexto = request.POST.get('questaotexto')
    if questaotexto == '':
        return render(request, 'votacao/criarquestao.html', {'error_message': "Não escreveu nenhuma Questão."})
    else:
        q = Questao.objects.create(questao_texto=questaotexto, pub_data=timezone.now())
        q.save()
        return HttpResponseRedirect(reverse('votacao:index'))

def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/criaropcao.html', {'questao': questao})


def submeteropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    opcaotexto = request.POST.get('opcaotexto')
    if opcaotexto == ''or opcaotexto is None:
        return render(request, 'votacao/criaropcao.html', {'questao': questao, 'error_message': "Não escreveu nenhuma Opção."})
    else:
        o = Opcao.objects.create(questao=questao, opcao_texto=opcaotexto, votos=0)
        o.save()
        return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))

def deletequestao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    questao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))

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

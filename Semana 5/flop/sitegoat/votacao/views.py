from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import Questao, Opcao
from django.template import loader
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    latest_question_list =Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'votacao/index.html',context)

def criarquestao(request):
    return render(request, 'votacao/criarquestao.html')

def detalhe(request, questao_id):
    """
    try:
        questao = Questao.objects.get(pk=questao_id)
    except Questao.DoesNotExist:
        raise Http404("A questao nao existe")
    """
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})
def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request,'votacao/resultados.html',{'questao': questao})


def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada =questao.opcao_set.get(pk=request.POST['opcao'])

    except (KeyError, Opcao.DoesNotExist):
    # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {
            'questao': questao,
            'error_message': "Não escolheu uma opção",
        })
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
     # Retorne sempre HttpResponseRedirect depois de
     # tratar os dados POST de um form
     # pois isso impede os dados de serem tratados
     # repetidamente se o utilizador
     # voltar para a página web anterior.
    return HttpResponseRedirect(reverse('votacao:resultados',args=(questao.id,)))


def submeterquestao(request):
    questaotexto = request.POST.get('resposta')
    q= Questao(questao_texto=questaotexto, pub_data=timezone.now())
    q.save()
    return index(request)
"""
def submeterquestao(request):
    if request.method == 'POST':
        questaotexto = request.POST.get('questaotexto', '')  # Safely get questaotexto from POST data
        print(questaotexto)

        if questaotexto:  # Check if questaotexto is not empty
            q = Questao(questao_texto=questaotexto, pub_data=timezone.now())
            q.save()
            return index(request)  # Assuming 'index' is the name of your index view
        else:
            # Handle case where questaotexto is empty
            print(teste)
            return index(request)

    else:
        # Handle GET request (if needed)
        return index(request)
"""
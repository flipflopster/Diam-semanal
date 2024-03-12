from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Questao, Opcao
from django.template import loader


def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    # template = loader.get_template('votacao/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    #  return HttpResponse(template.render(context, request))
    return render(request, 'votacao/index.html', context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


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
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
    return HttpResponseRedirect(
        reverse('votacao:resultados', args=(questao.id,)))

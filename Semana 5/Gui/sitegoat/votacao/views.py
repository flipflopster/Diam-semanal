from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Questao


def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def resultados(request, questao_id):
    response = "Estes sao os resultados da questao %s."
    return HttpResponse(response % questao_id)


def voto(request, questao_id):
    return HttpResponse("Votacao na questao %s." % questao_id)


def index(request):
    return HttpResponse("Pagina de entrada da app votacao.")

# Create your views here.

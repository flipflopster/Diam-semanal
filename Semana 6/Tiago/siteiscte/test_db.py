import datetime

from votacao.models import Questao
from votacao.models import Opcao
from django.utils import timezone


def questaolist():
    print("a) Mostrar uma lista com o texto de todas as questoes em BD")
    for questao in Questao.objects.all():
        print(questao)
    print()


def opcaolistfiltrada():
    print("b) Mostrar as opcoes da questao em que o texto comeca com /Gostas de .../")
    for opcao in Opcao.objects.all():
        if 'Gostas de' in opcao.questao.questao_texto:
            print(opcao)
    print()


def votosopcaolistfiltrada():
    print("c) Mostrar as opcoes com numero de votos superior a 2 da questao em que o texto comeca com /Gostas de .../")
    for opcaoVoto in Opcao.objects.all():
        if 'Gostas de' in opcaoVoto.questao.questao_texto and opcaoVoto.votos > 2:
            print(opcaoVoto.opcao_texto + " =", opcaoVoto.votos)
    print()


def questaolistfiltradatempo():
    print("d) Mostrar uma lista das questoes publicadas nos ultimos 3 anos")
    for questaotempo in Questao.objects.all():
        if questaotempo.pub_data >= timezone.now() - datetime.timedelta(days=1095):
            print(questaotempo)
    print()


def totaldevotos():
    print("e) Calcular e mostrar o numero total de votos que estao registados na base de dados")
    x = 0
    for questaoopcao in Opcao.objects.all():
        x += questaoopcao.votos
    print("Numero total do votos das questoes =", x)
    print()


def mostrarquestoesopcoes():
    print("f) Percorrer todas as questoes da DB e, para cada uma, mostrar o texto da questao e o da opcao que tiver "
          "mais votos")
    for x in Questao.objects.all():
        print(x.questao_texto)
        valor = 0
        for y in Opcao.objects.all():
            if y.votos > valor and y.questao == x:
                valor = y.votos
        for y in Opcao.objects.all():
            if y.votos == valor and y.questao == x:
                print(y.opcao_texto + " -", y.votos)
    print()


questaolist()
opcaolistfiltrada()
votosopcaolistfiltrada()
questaolistfiltradatempo()
totaldevotos()
mostrarquestoesopcoes()

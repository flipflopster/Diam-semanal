from votacao.models import Questao, Opcao

print("Exercicio 4.3:")

def exca():
    queryset, rList = Questao.objects.all(), []
    for q in queryset:
        print(q)

print('a)'); exca()

def excb():
    queryset, rList = Questao.objects.filter(questao_texto__startswith='Gostas de'), []
    for q in queryset:
        print(q)

print('\na)'); excb()

def excc():
    queryset, rList = Questao.objects.filter(questao_texto__startswith='Gostas de'), []
    for q in queryset:
        print(q)

print('\na)'); excc()
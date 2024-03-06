from votacao.models import Questao, Opcao
from django.utils import timezone

print("Exercicio 4.3:")

def exca():
    queryset = Questao.objects.all()
    for q in queryset:
        print(q)

print('a)'); exca()

def excb():
    queryset = Questao.objects.filter(questao_texto__startswith='Gostas de')
    for q in queryset:
        print(q)

print('\nb)'); excb()

def excc():
    queryset, rList = Questao.objects.filter(questao_texto__startswith='Gostas de').values_list('id', flat=True), []
    for q in queryset:
        rList.append(Opcao.objects.filter(questao = q).filter(votos__gt = 2))
    for r in rList:
        for o in r:
            print(o)

print('\nc)'); excc()

def excd():
    three_years_ago = timezone.now() - timezone.timedelta(days=365 * 3)
    queryset, rList = Questao.objects.filter(pub_data__gt=three_years_ago), []
    for q in queryset:
        rList.append(q)
    print(rList)

print('\nd)'); excd()

def exce():
    queryset, count = Questao.objects.all().values_list('id', flat=True), 0
    for q in queryset:
        for o in Opcao.objects.filter(questao=q).values_list('votos', flat=True):
            count += o
    print('Total de votos = ', o)

print('\ne)'); exce()

def excf():
    questoes = Questao.objects.all().values_list('questao_texto', flat=True)
    queryset, oList = Questao.objects.all().values_list('id', flat=True), []
    for q in queryset:
        if len(Opcao.objects.filter(questao=q)) > 1:
            fo = Opcao.objects.filter(questao=q).first()
            for o in Opcao.objects.filter(questao=q):
                if o.votos > fo.votos:
                    fo = o
        else:
            fo = 'Nao tem Opcoes.'
        oList.append(fo)
    for i in range(len(questoes)):
        print('Questao: ', questoes[i], ' Opcao com + votos: ', oList[i])

print('\nf)'); excf()
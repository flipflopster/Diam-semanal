from django.urls import include, path
from . import views

app_name = 'votacao'

urlpatterns = [
    # ex: votacao/
    path("", views.index, name='index'),
    # ex: votacao/1
    path('<int:questao_id>', views.detalhe, name='detalhe'),
    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados, name='resultados'),
    # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto, name='voto'),

    # criar uma nova questao
    path('criarquestao', views.criarquestao, name='criarquestao'),
    path('adicionarquestao', views.adicionarquestao, name='adicionarquestao'),

    # criar nova opçao para uma questao
    path('<int:questao_id>/criaropcao', views.criaropcao, name='criaropcao'),
    path('<int:questao_id>/adicionaropcao', views.adicionaropcao, name='adicionaropcao'),

    path('<int:questao_id>/removerquestao', views.removerquestao, name='removerquestao'),
    path('<int:questao_id>/removeropcao', views.removeropcao, name='removeropcao'),

]

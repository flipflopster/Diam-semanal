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

    # criar nova opçao para uma questao
    path('<int:questao_id>/criaropcao', views.criaropcao, name='criaropcao'),
    # path('<int:questao_id>/adicionaropcao', views.adicionaropcao, name='adicionaropcao'),

    # remover uma questao/opcao
    path('<int:questao_id>/removerquestao', views.removerquestao, name='removerquestao'),
    path('<int:questao_id>/removeropcao', views.removeropcao, name='removeropcao'),

    path('registar', views.registaruser, name='registaruser'),
    path('login', views.loginview, name='loginview'),
    path('meu_perfil', views.perfil, name='perfil'),
    path('logout', views.logoutview, name='logoutview'),
    path('fazer_upload', views.fazer_upload, name='fazer_upload'),
]

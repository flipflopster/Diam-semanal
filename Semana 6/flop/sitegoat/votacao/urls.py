from django.urls import path
from . import views

app_name = 'votacao'

# (. significa que importa views da mesma directoria)

urlpatterns = [
    # ex: votacao/
    path("", views.index, name='index'),
    # ex: votacao/1
    path('<int:questao_id>', views.detalhe, name='detalhe'),
    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados, name='resultados'),
    # ex: votacao/5/voto
    path('<int:questao_id>/trataropcao', views.trataropcao, name='trataropcao'),

    # criar questao
    path('criarquestao', views.criarquestao, name='criarquestao'),
    # submeter questao
    path('submeterquestao', views.submeterquestao, name='submeterquestao'),

    # criar opcao
    path('<int:questao_id>/criaropcao', views.criaropcao, name='criaropcao'),

    # submeter opcao
    path('<int:questao_id>/submeteropcao', views.submeteropcao, name='submeteropcao'),

    # apagar questao
    path('<int:questao_id>/deletequestao', views.deletequestao, name='deletequestao'),

    # fazer login
    path('login', views.fazerLogin, name='fazerLogin'),

    # fazer registo do user
    path('registar', views.registarUser, name='registarUser'),



]

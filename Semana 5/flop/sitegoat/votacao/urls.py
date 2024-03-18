from django.urls import include, path
from . import views

# (. significa que importa views da mesma directoria)
app_name = 'votacao'
urlpatterns = [
# ex: votacao/
    path("", views.index, name='index'),
 # ex: votacao/1
    path('<int:questao_id>', views.detalhe,name='detalhe'),
 # ex: votacao/3/resultados
    path('<int:questao_id>/resultados',views.resultados, name='resultados'),
 # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto,name='voto'),

    path('criarquestao', views.criarquestao, name='criarquestao'),

    path('submeterquestao', views.submeterquestao, name='submeterquestao'),

    path('<int:questao_id>/criarvoto', views.criarvoto, name='criarvoto'),

    path('<int:questao_id>/apagarvoto', views.apagarvoto, name='apagarvoto'),

    path('<int:questao_id>/jjkvoto', views.jjkvoto, name='jjkvoto'),

    path('<int:questao_id>/submetervoto', views.submetervoto, name='submetervoto'),
]
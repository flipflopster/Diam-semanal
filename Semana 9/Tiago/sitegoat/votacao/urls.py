from django.urls import path

from sitegoat.views import LoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static

#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = 'votacao'

# (. significa que importa views da mesma directoria)

urlpatterns = [

    # ex: votacao/
    path("", views.index, name='index'),

    path("uploadpp", views.uploadpp, name='uploadpp'),

    path("loadLogin", views.loadLogin, name='loadLogin'),
    path("loginPage", views.loginPage, name='loginPage'),

    path("userPage", views.userPage, name='userPage'),
    path("logoutview", views.logoutview, name='logoutview'),

    path("registar", views.registar, name='registar'),
    path("loadRegistar", views.loadRegistar, name='loadRegistar'),

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

    path('login/', LoginView.as_view(), name='login'),
]

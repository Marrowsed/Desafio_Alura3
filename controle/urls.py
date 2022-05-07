from django.urls import path
from controle.views import *
urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>', detalhes, name='detalhes'),
    #URLs de acesso
    path('cadastro', cadastro, name="cadastro"),
    path('login', entrar, name='login'),
    path('logout', sair, name='logout'),
    #URLs do usuário
    path('usuarios', usuarios, name='usuarios'),
    path('usuarios/cria', cria_usuario, name='criar_usuario'),
    path('usuario/deleta/<int:pk>', deleta_usuario, name='deleta_usuario'),
    path('usuario/edita/<int:pk>', edita_usuario, name='edita_usuario'),
]
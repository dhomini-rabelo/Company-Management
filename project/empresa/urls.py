from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('minha-conta/', minha_conta, name='minha_conta'),
    path('minha-conta/editar/', editar_conta, name='editar_conta'),
    path('minha-conta/nova-empresa/', nova_empresa, name='nova_empresa'),
    path('minha-conta/nova-empresa/cadastro-empresa', cadastro_empresa, name='cadastro_empresa'),
    path('minha-conta/nova-empresa/entrar-em-empresa', entrar_empresa, name='entrar_empresa'),
    path('minha-conta/nova-empresa/cadastro-gestor', cadastro_gestor, name='cadastro_gestor'),
    path('minha-conta/<str:link>/', info_empresa, name='info_empresa'),
    path('minha-conta/<str:link>/funcionarios', lista_funcionarios, name='lista_funcionarios'),
    path('minha-conta/<str:link>/funcionarios/<int:id>', funcionario, name='funcionario'),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('suporte', suporte, name='suporte'),
    path('minha-conta/', minha_conta, name='minha_conta'),
    path('minha-conta/meus-gestores', meus_gestores, name='meus_gestores'),
    path('minha-conta/editar/', editar_conta, name='editar_conta'),
    path('minha-conta/editar-empresa/', escolha_empresa, name='escolha_empresa'),
    path('minha-conta/editar-empresa/<str:link>', editar_empresa, name='editar_empresa'),
    path('minha-conta/nova-empresa/', nova_empresa, name='nova_empresa'),
    path('minha-conta/nova-empresa/cadastro-empresa', cadastro_empresa, name='cadastro_empresa'),
    path('minha-conta/nova-empresa/entrar-em-empresa', entrar_empresa, name='entrar_empresa'),
    path('minha-conta/<str:link>/cadastro-gestor', cadastro_gestor, name='cadastro_gestor'),
    path('minha-conta/<str:link>/', info_empresa, name='info_empresa'),
    path('minha-conta/<str:link>/funcionarios', lista_funcionarios, name='lista_funcionarios'),
    path('minha-conta/<str:link>/funcionarios/<int:id>', funcionario, name='funcionario'),
    path('minha-conta/<str:link>/funcionarios/recontratar/<int:id>', recontratar, name='recontratar'),
    path('minha-conta/<str:link>/funcionarios/<int:id>/editar', editar_funcionario, name='editar_funcionario'),
    path('minha-conta/<str:link>/funcionarios/cadastro-funcionario', cadastro_funcionario, name='cadastro_funcionario'),
]

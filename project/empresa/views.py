from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from decimal import Decimal
from account.support import *
from .models import *


def home(request):
    return render(request, 'home.html')


@login_required
def minha_conta(request):
    user = auth.get_user(request)
    context = dict()
    
    if user.empresario:
        empresas_presidente = Empresa.objects.filter(presidente=user)
        context['empresas_presidente'] = empresas_presidente
    if is_funcionario(user):
        funcionario = Funcionario.objects.filter(codigo=user.id)
        empresas_funcionario = Empresa.objects.filter(Funcionario=funcionario)
        context['empresas_funcionario'] = empresas_funcionario    
    
    return render(request, 'minha_conta.html', context)


@login_required
def editar_conta(request):
    if request.method != 'POST':
        return render(request, 'editar_conta.html')
    
    usuario = request.POST.get('usuario')
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha_atual = request.POST.get('senha_atual')
    nova_senha = request.POST.get('nova_senha')
    nova_senha2 = request.POST.get('nova_senha2')
    
    user = auth.get_user(request)
    if (usuario is not None) and usuario  != '':
        user.username = usuario
        messages.add_message(request, messages.SUCCESS, 'Novo nome de usuário cadastrado')
    elif (nome is not None) and nome != '':
        user.first_name = nome
        messages.add_message(request, messages.SUCCESS, 'Novo nome cadastrado')
    elif (email is not None) and email != '':
        try:
            validate_email(email)
            user.email = email
            messages.add_message(request, messages.SUCCESS, 'Novo email cadastrado')
        except:
            messages.add_message(request, messages.ERROR, 'Email inválido')
    elif not checks_null([senha_atual, nova_senha, nova_senha2]):
        if user.check_password(senha_atual) and nova_senha == nova_senha2 and len(nova_senha) > 5 and validate_caracteres(nova_senha):
            user.set_password(nova_senha)
            messages.add_message(request, messages.SUCCESS, 'Nova senha cadastrada')
        else:
            messages.add_message(request, messages.ERROR, 'Senha inválida')
            
    user.save()    
    return redirect('editar_conta')


@login_required
def nova_empresa(request):
    return render(request, 'nova_empresa.html')


@login_required
def info_empresa(request, link):
    context = dict()
    empresa = Empresa.objects.filter(link=link)
    context['empresa'] = empresa.first
    return render(request, 'info_empresa.html', context)


@login_required
def lista_funcionarios(request, link):
    context = dict()
    empresa = Empresa.objects.get(link=link)        
    context['empresa'] = empresa
    funcionarios_model = empresa.funcionarios.filter(demitido=False)
    
    nome = request.GET.get('nome')
    salario = request.GET.get('salario')
    profissao = request.GET.get('profissao')
    if nome is not None and nome.strip() != '':
        funcionarios_model = funcionarios_model.filter(nome__icontains=nome)
    if salario is not None and salario.strip() != '':
        funcionarios_model = funcionarios_model.filter(salario__lt=Decimal(salario))
    if profissao is not None and profissao.strip() != '':
        funcionarios_model = funcionarios_model.filter(profissao__icontains=profissao)
        
    funcionarios = [funcionario for funcionario in funcionarios_model]
    
    paginator = Paginator(funcionarios, 1)
    page_number = request.GET.get('p')
    funcionarios = paginator.get_page(page_number)
    
    context['funcionarios'] = funcionarios
    return render(request, 'lista_funcionarios.html', context)
    
    
@login_required
def funcionario(request, link, id):
    context = dict()
    context['funcionario'] = Funcionario.objects.get(id=id)
    context['empresa'] = Empresa.objects.get(link=link) 
    return render(request, 'funcionario.html', context)

        
"""
{% extends 'base.html' %}

{% block 'title' %}{% endblock %}

{% block  'content' %}
{% endblock %}

-----------------------

{% extends 'base.html' %}

{% block 'title' %}{% endblock %}

{% block  'content' %}
<div id="division">
    {% include 'Parts/_aside.html' %}
    <main>
    </main>
</div>
{% endblock %}
"""
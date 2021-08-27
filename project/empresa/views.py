from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from decimal import Decimal
from account.support import *
from .models import *
from .forms import EmpresaForm
from .support import *

def home(request):
    return render(request, 'home.html')


@login_required
def minha_conta(request):
    user = auth.get_user(request)
    context = dict()
    
    if user.empresario:
        empresas_presidente = Empresa.objects.filter(presidente=user)
        solicitacoes_empresa = list()
        for empresa in empresas_presidente:
            print(empresa)
            if empresa is not None:
                solicitacao = Solicitacao.objects.get(empresa=empresa)
            if solicitacao is not None:
                solicitacoes_empresa.append(solicitacao)
                
        context['solicitacoes_empresa'] = solicitacoes_empresa
        context['empresas_presidente'] = empresas_presidente
        
    if is_funcionario(user):
        funcionario = Funcionario.objects.filter(codigo=user.id)
        empresas_funcionario = Empresa.objects.filter(Funcionario=funcionario)
        
        solicitacoes_funcionario = list()
        for empresa in empresas_funcionario:
            solicitacao = Solicitacao.objects.get(usuario=user, resposta='nenhuma', status='em_andamento')
            if solicitacao is not None:
                solicitacoes_funcionario.append(solicitacao)
                
        context['solicitacoes_funcionario'] = solicitacoes_funcionario
        context['empresas_funcionario'] = empresas_funcionario 
        
    contexts = ['empresas_funcionario', 'empresas_presidente', 'solicitacoes_funcionario', 'empresas_presidente']
    if is_none_dict(context, contexts):
        return redirect('nova_empresa')
    
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
def entrar_empresa(request):
    user = auth.get_user(request)
    
    if request.method != 'POST':
        return render(request, 'entrar_empresa.html')
    
    nome_empresa = request.POST.get('nome_empresa')
    id_empresa = request.POST.get('id_empresa')
    
    if checks_null([nome_empresa, id_empresa]):
        empresa = Empresa.objects.get(nome=nome_empresa, id=id_empresa)
        print(empresa)
        if empresa is not None:
            Solicitacao.objects.create(usuario=user, empresa=empresa, status='em_andamento', resposta='nenhuma')
            messages.success(request, 'Solicitação criada com sucesso')
            return redirect('minha_conta')
        else:
            messages.error(request, 'Empresa não encontrada')
            return redirect('entrar_empresa')
        
    messages.error(request, 'Valores inválidos')
    return redirect('entrar_empresa')


@login_required
def cadastro_empresa(request):
    user = auth.get_user(request)
    context = dict()
    context['form'] = EmpresaForm
    if request.method != 'POST':
        return render(request, 'cadastro_empresa.html', context)
    
    nome = request.POST.get('nome')
    context['form'] = EmpresaForm(request.POST, request.FILES)
    
    logo = request.POST.get('logo')
    if checks_null([logo]):
        logo = 'images/logo.jpg'
        
    foto = request.POST.get('foto')
    if checks_null([foto]):
        foto = 'images/empresa.jpg'
    
    descricao = request.POST.get('descricao')
    data_de_criacao = request.POST.get('data_de_criacao')
    fundador = request.POST.get('fundador')
    valor = request.POST.get('valor')
    
    if not validate_cadastro_empresa(request, nome, descricao, data_de_criacao, fundador, valor):
        return render(request, 'cadastro_empresa.html', context)
    
    link =  set_slug(nome.replace(' ', '-').lower())
    
    Empresa.objects.create(nome=nome, logo=logo, foto=foto, descricao=descricao, data_de_criacao=data_de_criacao,
                           fundador=fundador, valor=valor, presidente=user, link=link)
    
    return redirect('minha_conta')


@login_required
def info_empresa(request, link):
    context = dict()
    empresa = Empresa.objects.filter(link=link)
    context['empresa'] = empresa.first
    return render(request, 'info_empresa.html', context)


@login_required
def lista_funcionarios(request, link):
    context = dict()
    empresa = Empresa.objects.get(link='arroz')        
    context['empresa'] = empresa
    funcionarios = empresa.funcionarios.filter(demitido=False).order_by('nome')
    
    nome = request.GET.get('nome')
    salario = request.GET.get('salario')
    profissao = request.GET.get('profissao')

    if nome is not None and nome.strip() != '':
        funcionarios = funcionarios.filter(nome__icontains=nome)
    if profissao is not None and profissao.strip() != '':
        funcionarios = funcionarios.filter(profissao__icontains=profissao)
    if salario is not None and salario.strip() != '':
        funcionarios = funcionarios.filter(salario__gte=Decimal(salario)).order_by('salario')
    
    paginator = Paginator(funcionarios, 15)
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
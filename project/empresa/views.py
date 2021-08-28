from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from decimal import Decimal
from account.support import *
from .models import *
from .forms import EmpresaForm, GestorForm
from .support import *
from django.utils import timezone

def home(request):
    return render(request, 'home.html')


@login_required
def minha_conta(request):
    user = auth.get_user(request)
    context = dict()
    if request.method == 'POST':
        # funcionario
        status = request.POST.get('status')
        id_solicitacao = request.POST.get('solicitacao')
        if not checks_null([id_solicitacao, status]):
            edit_solicitacao = Solicitacao.objects.get(id=id_solicitacao)
            edit_solicitacao.status = status
            edit_solicitacao.save()
        # empresario
        resposta = request.POST.get('resposta')
        id_solicitacao_empresa = request.POST.get('solicitacao_empresa')
        if not checks_null([id_solicitacao_empresa, resposta]):
            edit_solicitacao_empresa = Solicitacao.objects.get(id=id_solicitacao_empresa)
            edit_solicitacao_empresa.resposta = 'aceito' if resposta == 'sim' else 'recusado'
            edit_solicitacao_empresa.status = 'respondido'
            edit_solicitacao_empresa.save()
        
        
    solicitacoes_funcionario = list()
    solicitacoes = Solicitacao.objects.filter(usuario=user).exclude(status='finalizado')
    if not checks_null([solicitacoes]):
        for solicitacao in solicitacoes:
            solicitacoes_funcionario.append(solicitacao)
            
    context['solicitacoes_funcionario'] = solicitacoes_funcionario
    
    if user.empresario:
        empresas_presidente = Empresa.objects.filter(presidente=user)
        solicitacoes_empresa = list()
        for empresa in empresas_presidente:
            solicitacoes = Solicitacao.objects.filter(empresa=empresa, resposta='nenhuma', status='em_andamento')
            if not checks_null([solicitacoes]):
                for solicitacao in solicitacoes:
                    solicitacoes_empresa.append(solicitacao)
        context['solicitacoes_empresa'] = solicitacoes_empresa
        context['empresas_presidente'] = empresas_presidente
        
    if is_funcionario(user):
        empresas_funcionario = list()
        profissoes = list()
        funcionario = Funcionario.objects.filter(codigo=user.id)[0]
        solicitacoes_aceitas = Solicitacao.objects.filter(usuario=user, status='finalizado', resposta='aceito')
        for solicitacao in solicitacoes_aceitas:
            funcionarios_empresa_solicitada = solicitacao.empresa.funcionarios.all()
            for funcionario_empresa in funcionarios_empresa_solicitada:
                if funcionario_empresa == funcionario:
                    profissoes.append(funcionario.profissao)
                    empresas_funcionario.append(solicitacao.empresa)
                    break
        profissoes.append('hello')
        context['profissoes'] = iter(profissoes)
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
def cadastro_gestor(request, link):
    context = dict()
    if request.method != 'POST':
        context['form'] = GestorForm
        return render(request, 'cadastro_gestor.html', context)
        
    user = auth.get_user(request)
    empresa = Empresa.objects.filter(link=link)[0]
    solicitacao = Solicitacao.objects.get(empresa=empresa, usuario=user)

    nome = request.POST.get('nome_user')
    email = request.POST.get('email_user')
    foto = user.foto
    codigo = user.id
    idade = request.POST.get('idade')
    salario = request.POST.get('salario')
    telefone_pessoal = request.POST.get('telefone_pessoal')
    telefone_comercial = request.POST.get('telefone_comercial')
    cpf = request.POST.get('cpf')
    profissao = request.POST.get('profissao')
    bio = request.POST.get('bio')
    
    if validate_cadastro_gestor(request, nome, email, foto, codigo,  idade, salario, telefone_pessoal, telefone_comercial, cpf, profissao, bio):
        Funcionario.objects.create(nome=nome, idade=idade, foto=foto, email=email, codigo=codigo, salario=salario, telefone_pessoal=telefone_pessoal, telefone_comercial=telefone_comercial, cpf=cpf, profissao=profissao, bio=bio, ultima_mudanca=timezone.now, data_registro=timezone.now, demitido=False)
        solicitacao.status = 'finalizado'
        solicitacao.save()
        empresa.funcionarios.add(Funcionario.objects.get(codigo=user.id))
        empresa.save()
        return redirect('minha_conta')
    else:
        context['form'] = GestorForm(request.POST)
        return render(request, 'cadastro_gestor.html', context)
        
    

@login_required
def entrar_empresa(request):
    if request.method != 'POST':
        return render(request, 'entrar_empresa.html')
    
    user = auth.get_user(request)
    
    nome_empresa = request.POST.get('nome_empresa')
    id_empresa = request.POST.get('id_empresa')
    
    if not checks_null([nome_empresa, id_empresa]):
        empresa = Empresa.objects.filter(nome=nome_empresa, id=id_empresa)
        if not checks_null([empresa]):
            Solicitacao.objects.create(usuario=user, empresa=empresa[0], status='em_andamento', resposta='nenhuma')
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
    empresa = Empresa.objects.get(link=link) # error 404 se nao char link        
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
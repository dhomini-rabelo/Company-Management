from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from decimal import Decimal
from account.support import is_funcionario, validate_for_email, validate_email, validate_caracteres
from .models import Empresa, Funcionario, Solicitacao, get_codigo
from .forms import EmpresaForm, FuncionarioForm, GestorForm, ImageForm
from .support import checks_null, is_none_dict, permission, check_invalid_decimal, check_invalid_date, validate_cpf, validate_cadastro_gestor, validate_cadastro_empresa, set_slug
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
        context['profissoes'] = iter(profissoes)
        context['empresas_funcionario'] = empresas_funcionario
        
        
    contexts = ['empresas_funcionario', 'empresas_presidente', 'solicitacoes_funcionario', 'empresas_presidente']
    if is_none_dict(context, contexts):
        return redirect('nova_empresa')
    return render(request, 'minha_conta.html', context)


@login_required
def editar_conta(request):
    if request.method != 'POST':
        context = {'image_form': ImageForm}
        return render(request, 'editar_conta.html', context)
    
    usuario = request.POST.get('usuario')
    nome = request.POST.get('nome')
    foto = request.FILES.get('image')
    email = request.POST.get('email')
    senha_atual = request.POST.get('senha_atual')
    nova_senha = request.POST.get('nova_senha')
    nova_senha2 = request.POST.get('nova_senha2')
    
    user = auth.get_user(request)
    if (str(foto) is not None) and str(foto) != '':
        user.foto = foto
    elif (usuario is not None) and usuario  != '':
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
def meus_gestores(request):
    user = auth.get_user(request)
    context = dict()
    if user.empresario:
        empresas = Empresa.objects.filter(presidente=user)
        context['empresas_presidente'] = empresas
    return render(request, 'meus_gestores.html', context)

@login_required
def editar_empresa(request, link):
    if not permission(request, link):
        return redirect('minha_conta')
    
    user = auth.get_user(request)    
    context = dict()
    empresa = Empresa.objects.get(link=link) 
    context['empresa'] = empresa
    if request.method != 'POST':
        return render(request, 'editar_empresa.html', context)
    
    apagar = request.POST.get('apagar')
    if apagar == 'sim':
        messages.success(request, f'{empresa.nome} foi apagada')
        empresa.delete()
        if len(Empresa.presidente.filter(presidente=user)) == 0:
            user.empresario = False
            user.save()
        return redirect('escolha_empresa')
    
    nome = request.POST.get('nome')
    logo = request.FILES.get('logo')
    foto = request.FILES.get('foto')
    descricao = request.POST.get('descricao')
    data_de_criacao = request.POST.get('data_de_criacao')
    fundador = request.POST.get('fundador')
    valor = request.POST.get('valor')
    
    if (foto is not None) and str(foto) != 'None':
        empresa.foto = foto
    if (logo is not None) and str(logo) != 'None':
        empresa.logo = logo
    if (nome is not None) and nome != '':
        empresa.nome = nome
    if (data_de_criacao is not None) and data_de_criacao != '' and (not check_invalid_date(data_de_criacao)):
        empresa.data_de_criacao = data_de_criacao
    if (descricao is not None) and descricao != '':
        empresa.descricao = descricao
    if (fundador is not None) and fundador != '':
        empresa.fundador = fundador
    if (valor is not None) and (not check_invalid_decimal(valor)):
        empresa.valor = valor
    
    empresa.save()    
    return redirect('info_empresa', empresa.link)

@login_required
def escolha_empresa(request):
    user = auth.get_user(request)
    context = dict()
    if user.empresario:
        context['empresas_presidente'] = Empresa.objects.filter(presidente=user)
    return render(request, 'escolha_empresa.html', context)
        

@login_required
def editar_funcionario(request, link, id):
    if not permission(request, link):
        return redirect('minha_conta')
        
    context = dict()
    funcionario = get_object_or_404(Funcionario, id=id)
    empresa = Empresa.objects.get(link=link) 
    context['funcionario'] = funcionario
    context['empresa'] = empresa 
    if request.method != 'POST':
        return render(request, 'editar_funcionario.html', context)
    
    demitido = request.POST.get('demitido')
    if demitido == 'sim':
        funcionario.demitido = True
        funcionario.save()
        messages.success(request, f'{funcionario} demitido')
        return redirect('lista_funcionarios', empresa.link)
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    foto = request.FILES.get('foto')
    idade = request.POST.get('idade')
    salario = request.POST.get('salario')
    telefone_pessoal = request.POST.get('telefone_pessoal')
    telefone_comercial = request.POST.get('telefone_comercial')
    cpf = request.POST.get('cpf')
    profissao = request.POST.get('profissao')
    bio = request.POST.get('bio')
    
    if (foto is not None) and str(foto) != 'None':
        funcionario.foto = foto
    if (nome is not None) and nome != '':
        funcionario.nome = nome
    if (profissao is not None) and profissao != '':
        funcionario.profissao = profissao
    if (bio is not None) and bio != '':
        funcionario.bio = bio
    if (telefone_pessoal is not None) and telefone_pessoal != '':
        funcionario.telefone_pessoal = telefone_pessoal
    if (telefone_comercial is not None) and telefone_comercial != '':
        funcionario.telefone_comercial = telefone_comercial
    if (email is not None) and email != '' and validate_for_email(email):
        funcionario.email = email
    if (cpf is not None) and cpf != '' and (not validate_cpf(cpf)):
        funcionario.cpf = cpf
    if (idade is not None) and (not check_invalid_decimal(idade)):
        funcionario.idade = idade
    if (salario is not None) and (not check_invalid_decimal(salario)):
        funcionario.salario = salario

    funcionario.save()
    return redirect('funcionario', empresa.link, funcionario.id)
    
    

@login_required
def cadastro_funcionario(request, link):
    if not permission(request, link):
        return redirect('minha_conta')
            
    context = dict()
    context['form'] = FuncionarioForm
    empresa = Empresa.objects.get(link=link)
    context['empresa'] = empresa
    if request.method != 'POST':
        return render(request, 'cadastro_funcionario.html', context)
    
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    foto = request.FILES.get('foto')
    if foto is not None and checks_null([foto]):
        foto = 'images/default.jpg'
    idade = request.POST.get('idade')
    codigo = get_codigo()
    salario = request.POST.get('salario')
    telefone_pessoal = request.POST.get('telefone_pessoal')
    telefone_comercial = request.POST.get('telefone_comercial')
    cpf = request.POST.get('cpf')
    profissao = request.POST.get('profissao')
    bio = request.POST.get('bio')
    
    if validate_cadastro_gestor(request, nome, email, foto, codigo, idade, salario, telefone_pessoal, telefone_comercial, cpf, profissao, bio):
        Funcionario.objects.create(
            nome=nome, idade=idade, foto=foto, email=email, codigo=codigo, salario=salario, 
            telefone_pessoal=telefone_pessoal, telefone_comercial=telefone_comercial, cpf=cpf, 
            profissao=profissao, bio=bio, ultima_mudanca=timezone.now, data_registro=timezone.now, demitido=False
        )
        empresa.funcionarios.add(Funcionario.objects.get(codigo=codigo))
        empresa.save()
        return redirect('lista_funcionarios', link=link)
    else:
        context['form'] = FuncionarioForm(request.POST)
        return render(request, 'cadastro_funcionario.html', context)
    

@login_required
def cadastro_gestor(request, link):
    if not permission(request, link):
        return redirect('minha_conta')
            
    context = dict()
    user = auth.get_user(request)
    empresa = Empresa.objects.filter(link=link)[0]
    solicitacao = Solicitacao.objects.get(empresa=empresa, usuario=user)
    if request.method != 'POST':
        context['form'] = GestorForm
        if checks_null([Funcionario.objects.filter(codigo=user.id)]):
            return render(request, 'cadastro_gestor.html', context)
        else:
            solicitacao.status = 'finalizado'
            solicitacao.save()
            empresa.funcionarios.add(Funcionario.objects.get(codigo=user.id))
            empresa.save()
            return redirect('minha_conta')

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
        Funcionario.objects.create(
            nome=nome, idade=idade, foto=foto, email=email, codigo=codigo, salario=salario, 
            telefone_pessoal=telefone_pessoal, telefone_comercial=telefone_comercial, cpf=cpf, 
            profissao=profissao, bio=bio, ultima_mudanca=timezone.now, data_registro=timezone.now, demitido=False
        )
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
    minhas_empresas = [empresa for empresa in Empresa.objects.filter(presidente=user)]
    nome_empresa = request.POST.get('nome_empresa')
    id_empresa = request.POST.get('id_empresa')
    
    if not checks_null([nome_empresa, id_empresa]):
        empresa = Empresa.objects.filter(nome=nome_empresa, id=id_empresa)
        if not checks_null([empresa]) and empresa[0] not in minhas_empresas:
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
    repeated = len(Empresa.objects.filter(link=link))
    c = 2
    while repeated != 0:
            link += f'-{c}' if c == 2 else f'{c}'
            repeated = len(Empresa.objects.filter(link=link))

    Empresa.objects.create(nome=nome, logo=logo, foto=foto, descricao=descricao, data_de_criacao=data_de_criacao,
                           fundador=fundador, valor=valor, presidente=user, link=link)
    user.empresario = True
    user.save()
    return redirect('minha_conta')


@login_required
def info_empresa(request, link):
    if not permission(request, link):
        return redirect('minha_conta')
            
    context = dict()
    empresa = Empresa.objects.filter(link=link)
    context['empresa'] = empresa.first
    return render(request, 'info_empresa.html', context)


@login_required
def lista_funcionarios(request, link):
    if not permission(request, link):
        return redirect('minha_conta')
            
    context = dict()
    empresa = Empresa.objects.get(link=link)     
    context['empresa'] = empresa
    funcionarios = empresa.funcionarios.filter(demitido=False).order_by('nome')
    
    nome = request.GET.get('nome')
    salario = request.GET.get('salario')
    profissao = request.GET.get('profissao')
    demitido = request.GET.get('demitido')
    if demitido is not None and demitido == 'true':
        funcionarios = empresa.funcionarios.filter(demitido=True).order_by('nome')
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
    if not permission(request, link):
        return redirect('minha_conta')
            
    context = dict()
    funcionario = Funcionario.objects.get(id=id)
    empresa = Empresa.objects.get(link=link)
    if funcionario.demitido == True:
        return redirect('recontratar', empresa.link, funcionario.id)
    
    context['funcionario'] = funcionario
    context['empresa'] = empresa 
    return render(request, 'funcionario.html', context)


@login_required
def recontratar(request, link, id):
    if not permission(request, link):
        return redirect('minha_conta')
    context = dict()
    funcionario = Funcionario.objects.get(id=id)
    empresa = Empresa.objects.get(link=link)
    if funcionario.demitido == False:
        return redirect('funcionario', empresa.link, funcionario.id)
    
    context['funcionario'] = funcionario
    context['empresa'] = empresa 
    if request.method != 'POST':
        return render(request, 'recontratar.html', context)
    
    resposta = request.POST.get('resposta')
    if resposta is None:
        return render(request, 'recontratar.html', context)
    elif resposta == 'sim':
        funcionario.demitido = False
        funcionario.save()
        messages.success(request, f'{funcionario.nome} recontratado')
        return redirect('funcionario', empresa.link, funcionario.id)
    else:
        return redirect('lista_funcionarios', empresa.link)

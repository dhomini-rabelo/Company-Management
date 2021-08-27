# Usuário
from django.contrib.auth.models import User
from django.contrib import messages, auth
from .support import *
# Renderizar
from django.shortcuts import render, redirect

def login(request):
    user = auth.get_user(request)
    
    if user.is_authenticated:
        return redirect('minha_conta')
    elif request.method != 'POST':
        return render(request, 'login.html')
    
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)
    
    if user is None:
        messages.add_message(request, messages.ERROR, 'Usuário ou senha inválidos')
        return redirect('login')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Login realizado com sucesso')
        return redirect('minha_conta')


def cadastro(request):
    user = auth.get_user(request)
    if user.is_authenticated:
        return redirect('minha_conta')
    elif request.method != 'POST':
        return render(request, 'cadastro.html')
    
    foto = request.POST.get('foto')
    if checks_null([foto]):
        foto = 'images/empresa.jpg'
    nome = request.POST.get('nome').title()
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    
    
    if not validate_cadastro_usuario(request, usuario, senha, senha2, nome, email):
        return redirect('cadastro')
    
    new_user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name='', foto=foto)
    new_user.save()
    messages.add_message(request, messages.SUCCESS, f'{usuario} foi registrado com sucesso')
    return redirect('login')


def logout(request):
    auth.logout(request)
    return redirect('login')
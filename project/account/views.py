# Usuário
from django.contrib.auth.models import User
from django.contrib import messages, auth
from .support import *
# Renderizar
from django.shortcuts import render, redirect

def login(request):
    user = auth.get_user(request)
    
    if user.is_authenticated:
        return redirect('minha_conta_adm')
    elif request.method != 'POST':
        return render(request, 'login.html')
    
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)
    
    if user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Usuário ou senha inválidos')
        return redirect(request, 'login.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Login realizado com sucesso')
        return redirect('minha_conta_adm')


def cadastro(request):
    user = auth.get_user(request)
    if user.is_authenticated:
        return redirect('minha_conta_adm')
    elif request.method != 'POST':
        return render(request, 'cadastro_adm.html')
    
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    inputs = [nome, email, usuario, senha, senha2]
    
    if not (validate_form(request, inputs, email) and validate_login(request, usuario, senha, senha2)):
        return render(request, 'cadastro_adm.html')
    
    new_user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name='')
    new_user.save()
    messages.add_message(request, messages.SUCCESS, f'{usuario} foi registrado com sucesso')
    return redirect('login')


def logout(request):
    auth.logout(request)
    return redirect('login')
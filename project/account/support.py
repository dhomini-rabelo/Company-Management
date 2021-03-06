from django.core.validators import validate_email
from django.shortcuts import render
from django.contrib import messages, auth
from .models import User
from empresa.models import *
from string import ascii_letters, digits


def is_funcionario(user):
    res = Funcionario.objects.filter(codigo=user.id) # response
    if len(res) > 0:
        return True
    return False

def exist_session(request, session_name: str):
    try:
        if request.session[session_name]:
            return True
    except KeyError:
        return False
    
    
def user_make_login(request):
    user = auth.get_user(request)
    if user.is_authenticated:
        return True
    return False

def checks_null(input_list: list):
    for we in input_list:
        try:
            if we is None:
                return True
            elif isinstance(we, str) and we.strip() == '':
                return True
            elif len(we) == 0:
                return True
        except TypeError:
            pass
    return False


def validate_for_email(email: str):
    try:
        validate_email(email)
        return True
    except:
        return False

        
def validate_caracteres(text):
    symbols = "@.+-_"
    alloweds = symbols + digits + ascii_letters
    for letter in text:
       if letter not in alloweds:
           return False
    return True

        
def validate_login(request, usuario:str,  senha: str, senha2: str):
    if not validate_caracteres(usuario):
        messages.error(request, 'O nome de usuário contém caracteres inválidos')
    elif not validate_caracteres(senha):
        messages.error(request, 'A senha contém caracteres inválidos')
    elif len(senha) < 6:
        messages.error(request, 'Senha deve ter no mínimo 6 dígitos')
    elif senha != senha2:
        messages.error(request, 'As senhas não conferem')
    elif User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário existente')
    else:
        return True
    return False


def validate_cadastro_usuario(request, usuario:str,  senha: str, senha2: str, nome: str, email:str):
    inputs = [nome, email, usuario, senha, senha2]
    if checks_null(inputs):
        messages.error(request, 'Algum campo está vazio')
    elif not validate_for_email(email):
        messages.error(request, 'Email inválido')
    elif User.objects.filter(email=email).exists():
        messages.error(request, 'Email existente')
    elif not validate_login(request, usuario, senha, senha2):
        pass
    else:
        return True
    return False

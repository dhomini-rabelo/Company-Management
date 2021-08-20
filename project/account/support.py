from django.core.validators import validate_email
from django.shortcuts import render
from django.contrib import messages, auth
from django.contrib.auth.models import User


def exist_session(request, session_name: str):
    try:
        if request.session[session_name]:
            return True
    except KeyError:
        return False
    
    
def user_make_login(request):
    try:
        if request.auth.is_authenticated:
            return True
    except AttributeError:
        return False

def check_null_input(input_list: list):
    for we in input_list:
        if len(we) == 0 or we is None:
            return True
    return False

def validate_form(request, inputs: list, email:str):
    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'Email inválido')
        return False
    if check_null_input(inputs):
        messages.add_message(request, messages.ERROR, 'Algum campo está vazio')
    elif User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, 'email existente')
    else:
        return True
    return False
        
        
def validate_login(request, usuario:str,  senha: str, senha2: str):
    if len(senha) < 6:
        messages.add_message(request, messages.ERROR, 'Senha deve ter no mínimo 6 dígitos')
    elif senha != senha2:
        messages.add_message(request, messages.ERROR, 'As senhas não conferem')
    elif User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR, 'Usuário existente')
    else:
        return True
    return False
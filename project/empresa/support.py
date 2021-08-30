from django.core.validators import validate_slug, validate_unicode_slug 
from decimal import Decimal
from account.support import checks_null, validate_for_email
from django.contrib import messages, auth
from datetime import datetime
from .models import Funcionario, Empresa


def is_none_dict(dictionary: dict, objects: list):
    for obj in objects:
        if not checks_null([dictionary.get(obj)]):
            return False
    return True


def set_slug(slug: str):
    invalid_letters = list()
    slug_list = [letter for letter in slug]
    for letter in slug_list:
        try:
            validate_slug(letter)
            validate_unicode_slug(letter)
        except:
            invalid_letters.append(letter)
    for letter in invalid_letters:
        slug_list.remove(letter)
    return "".join(slug_list)


def check_invalid_decimal(value):
    try:
        Decimal(1.00) + Decimal(value)
        return False
    except:
        return True
    

def check_invalid_date(date: str):
    try:
        date_check = str(datetime.strptime(date, '%Y-%m-%d').date())
        return not date == date_check
    except:
        return True


def validate_cadastro_empresa(request, nome, descricao, data_de_criacao, fundador, valor):
    fields = [nome, descricao, data_de_criacao, fundador, valor]
    if checks_null(fields):
        messages.error(request, 'Algum campo não foi preenchido')
        return False
    elif check_invalid_decimal(valor):
        messages.error(request, 'Valor não é válido')
        return False
    elif check_invalid_date(data_de_criacao):
        messages.error(request, 'Valor não é válido')
        return False
    else: 
        return True


def validate_cpf(cpf):
    funcionario = Funcionario.objects.filter(cpf=cpf)
    if checks_null([funcionario]):
        return False
    return True
    
def validate_cadastro_gestor(request, nome, email, foto, codigo,  idade, salario, telefone_pessoal, telefone_comercial, cpf, profissao, bio):
    fields = [nome, email, foto, codigo, telefone_pessoal, telefone_comercial, cpf, profissao, bio]
    if checks_null(fields):
        messages.error(request, 'Algum campo não foi preenchido')
        return False
    elif check_invalid_decimal(salario):
        messages.error(request, 'Valor não é válido')
        return False
    elif check_invalid_decimal(idade):
        messages.error(request, 'Valor não é válido')
        return False
    elif not validate_for_email(email):
        messages.error(request, 'Email inválido')
        return False
    elif not validate_cpf(cpf):
        messages.error(request, 'CPF repetido')
        return False
    else:
        return True
    
    
def permission(request, link):
    user = auth.get_user(request)
    empresa = Empresa.objects.get(link=link) 
    funcionario = Funcionario.objects.filter(codigo=user.id)
    funcionarios = [funcionario for funcionario in empresa.funcionarios.all()]
    if empresa.presidente == user:
        return True
    elif funcionario[0] in funcionarios:
        return True
    else:
        return False
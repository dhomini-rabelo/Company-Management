from django.core.validators import validate_slug, validate_unicode_slug 
from decimal import Decimal
from account.support import checks_null
from django.contrib import messages
from datetime import datetime

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
    date_check = str(datetime.strptime(date, '%Y-%m-%d').date())
    return not date == date_check


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


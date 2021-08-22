from django.contrib import admin
from .models import *


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = 'icone', 'nome', 'telefone_comercial', 'salario'
    list_display_links = 'nome',
    list_filter = 'demitido',


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = 'logo', 'nome', 'presidente'
    list_display_links = 'nome',

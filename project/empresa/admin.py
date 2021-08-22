from django.contrib import admin
from .models import *


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = 'icone', 'nome', 'profissao', 'salario'
    list_display_links = 'nome',
    list_filter = 'demitido',


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = 'logo', 'nome', 'presidente', 'valor'
    list_display_links = 'nome',
    
    
@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = 'nome', 'valor', 'empresa',
    list_display_links = 'nome',
    

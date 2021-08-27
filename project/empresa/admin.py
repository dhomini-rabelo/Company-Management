from django.contrib import admin
from .models import *


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = 'icone', 'nome', 'profissao', 'salario'
    list_display_links = 'nome',
    list_filter = 'demitido',
    readonly_fields = 'codigo',
    search_fields = 'nome',
    list_per_page = 20


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = 'icone_logo', 'nome', 'presidente', 'valor', 'n_funcionarios', 'id'
    list_display_links = 'nome',
    
    
@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = 'nome', 'valor', 'empresa', 
    list_display_links = 'nome',
    
@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = 'usuario', 'empresa', 'status', 'resposta'
    list_display_links = 'status',
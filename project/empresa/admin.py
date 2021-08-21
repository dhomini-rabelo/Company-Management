from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = 'icone', 'nome', 'telefone_comercial', 'salario', 'admin'
    list_display_links = 'nome',
    list_filter = 'demitido',

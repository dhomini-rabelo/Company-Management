from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, DO_NOTHING, DecimalField, DateField, BooleanField, CASCADE)
from django.db.models.fields.related import ManyToManyField
from django.utils.safestring import mark_safe
from django.utils import timezone
from account.models import User
from django.db import models

class Funcionario(Model):
    nome = CharField(max_length=120)
    idade = PositiveIntegerField()
    foto = ImageField('Foto de perfil', upload_to='images/%Y/%m/%d/%M/%f', default='images/default.jpg')
    salario = DecimalField('Salário', max_digits=12, decimal_places=2)
    telefone_pessoal = CharField('Telefone pessoal', max_length=20, blank=True)
    telefone_comercial = CharField('Telefone de trabalho', max_length=25, blank=True)
    cpf = CharField('CPF', max_length=25, unique=True, blank=True)
    admin = ForeignKey(User, on_delete=CASCADE)
    data_registro = DateField('Data de registro', auto_now_add=True)
    demitido = BooleanField(default=False)
    ultima_mudanca = DateField('Última mudança', auto_now=True)
    
    def __str__(self):
        return self.nome
    
    @mark_safe
    def icone(self):
        return f'<a href="/media/{self.foto}" target="_blank"><img src="/media/{self.foto}" style="width: 35px; height: 25px;"></a>'
    
    
class Empresa(Model):
    nome = CharField(max_length=120)
    logo = ImageField(upload_to='images/company/%Y/%m/%d/%M/%f', blank=True)
    foto = ImageField(upload_to='images/company/%Y/%m/%d/%M/%f', blank=True)
    descricao = TextField('Descrição', blank=True) 
    presidente = ForeignKey(User, on_delete=CASCADE)
    funcionarios = ManyToManyField(Funcionario, verbose_name='Funcionários')
    despesas = DecimalField('Despesas Mensais', max_digits=12, decimal_places=2)
    data_de_criacao = DateField('Data de criação', blank=True)
    fundador = CharField(max_length=120, blank=True)
    
    
class Setor(Model):
    nome = CharField(max_length=120)
    empresa = ForeignKey(Empresa, on_delete=CASCADE)
    funcao = TextField('Função', blank=True) 
    funcionarios = ManyToManyField(Funcionario, verbose_name='Funcionários')
    descricao = TextField('Descrição', blank=True) 
    
    
class Tarefa(Model):
    nome = CharField(max_length=120)
    descricao = TextField('Descrição', blank=True) 
    finalizado = BooleanField(default=False)
    fases = PositiveIntegerField(blank=True)
    
    
class Etapa(Model):
    nome = CharField(max_length=120)
    descricao = TextField('Descrição', blank=True) 
    finalizado = BooleanField(default=False)
    tarefas = ManyToManyField(Tarefa)


class Projeto(Model):
    imagem_principal = ImageField(upload_to='images/project/%Y/%m/%d/%M/%f')
    titulo = CharField(max_length=120)
    descricao = TextField('Descrição') 
    gastos = DecimalField(max_digits=12, decimal_places=2)
    lucros = DecimalField(max_digits=12, decimal_places=2)
    empresa = ForeignKey(Empresa, on_delete=CASCADE)
    etapas = ManyToManyField(Etapa)
    funcionarios = ManyToManyField(Funcionario, verbose_name='Funcionários')
    
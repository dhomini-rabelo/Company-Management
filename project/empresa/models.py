from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, DO_NOTHING, DecimalField, DateField, BooleanField, CASCADE, PositiveBigIntegerField)
from django.db.models.fields import SlugField
from django.db.models.fields.related import ManyToManyField
from django.utils.safestring import mark_safe
from django.utils import timezone
from account.models import User
from django.db import models
from decimal import Decimal

def get_codigo():
    last_number = 9000000000000000000
    number = last_number - len(Funcionario.objects.all())
    return number

    
class Funcionario(Model):
    nome = CharField(max_length=120)
    idade = PositiveIntegerField()
    foto = ImageField('Foto de perfil', upload_to='images/%Y/%m/%d/%M/%f', default='images/default.jpg')
    salario = DecimalField('Salário', max_digits=12, decimal_places=2)
    telefone_pessoal = CharField('Telefone pessoal', max_length=20, blank=True)
    telefone_comercial = CharField('Telefone de trabalho', max_length=25, blank=True)
    cpf = CharField('CPF', max_length=25, unique=True, blank=True)
    data_registro = DateField('Data de registro', auto_now_add=True)
    demitido = BooleanField(default=False)
    ultima_mudanca = DateField('Última mudança', auto_now=True)
    profissao = CharField(max_length=120, default='desempregado')
    bio = TextField(default='', blank=True)
    codigo = PositiveBigIntegerField(unique=True, blank=True, default=get_codigo)
    
    def __str__(self):
        return self.nome
    
    @mark_safe
    def icone(self):
        return f'<a href="/media/{self.foto}" target="_blank"><img src="/media/{self.foto}" style="width: 35px; height: 25px;"></a>'


class Empresa(Model):
    nome = CharField(max_length=120)
    logo = ImageField(upload_to='images/company/%Y/%m/%d/%M/%f', default='images/logo.jpg')
    foto = ImageField(upload_to='images/company/%Y/%m/%d/%M/%f', default='images/empresa.jpg')
    descricao = TextField('Descrição', blank=True) 
    presidente = ForeignKey(User, on_delete=DO_NOTHING)
    funcionarios = ManyToManyField(Funcionario, verbose_name='Funcionários', blank=True)
    despesas = DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), blank=True)
    data_de_criacao = DateField('Data de criação', blank=True)
    fundador = CharField(max_length=120, blank=True)
    valor = DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), blank=True)
    link = SlugField(max_length=120, default='/', blank=True, unique=True)
    
    def __str__(self):
        return self.nome
    
    @mark_safe
    def icone_logo(self):
        return f'<a href="/media/{self.logo}" target="_blank"><img src="/media/{self.logo}" style="width: 35px; height: 25px;"></a>'
        
    @mark_safe
    def icone_foto(self):
        return f'<a href="/media/{self.foto}" target="_blank"><img src="/media/{self.foto}" style="width: 35px; height: 25px;"></a>'
 
    
class Despesa(Model):
    nome = CharField(max_length=120)
    descricao = TextField('Descrição', blank=True) 
    valor = DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), blank=True)
    empresa = ForeignKey(Empresa, on_delete=DO_NOTHING, blank=True, null=True)
    
# class Setor(Model):
#     nome = CharField(max_length=120)
#     empresa = ForeignKey(Empresa, on_delete=CASCADE)
#     funcao = TextField('Função', blank=True) 
#     funcionarios = ManyToManyField(Funcionario, verbose_name='Funcionários')
#     descricao = TextField('Descrição', blank=True) 
#     tarefas = ManyToManyField(Tarefa)
    
    
# class Tarefa(Model):
#     nome = CharField(max_length=120)
#     descricao = TextField('Descrição', blank=True) 
#     finalizado = BooleanField(default=False)
#     fases = PositiveIntegerField(blank=True)
#     gastos = DecimalField(max_digits=12, decimal_places=2) - prazo
    
    
# class Etapa(Model):
#     nome = CharField(max_length=120)
#     descricao = TextField('Descrição', blank=True) 
#     finalizado = BooleanField(default=False)
#     tarefas = ManyToManyField(Tarefa)


# class Projeto(Model):
#     imagem = ImageField(upload_to='images/project/%Y/%m/%d/%M/%f')
#     titulo = CharField(max_length=120)
#     descricao = TextField('Descrição') 
#     gastos = DecimalField(max_digits=12, decimal_places=2)
#     lucros = DecimalField(max_digits=12, decimal_places=2)
#     empresa = ForeignKey(Empresa, on_delete=CASCADE)
#     etapas = ManyToManyField(Etapa)
#     funcionarios = ManyToManyField(Funcionario, verbose_name='Funcionários') - prazo
#foto001 opcional
#foto001
#foto001
#foto001
#foto001
    
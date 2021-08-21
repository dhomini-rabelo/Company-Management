from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, DO_NOTHING, DecimalField, DateField, BooleanField, CASCADE)
from django.utils.safestring import mark_safe
from django.utils import timezone
from account.models import User

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
from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, DO_NOTHING, DecimalField, DateField, BooleanField)
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from django.utils import timezone

class User(AbstractUser):
    idade = PositiveIntegerField(blank=True)
    foto = ImageField('Foto de perfil', upload_to='images/%Y/%m/%d/%M/%f', blank=True, default='imagens/default.jpg')
    telefone_pessoal = CharField('Telefone pessoal', max_length=20, blank=True)
    telefone_comercial = CharField('Telefone de trabalho', max_length=25, blank=True)
    cpf = CharField('CPF', max_length=25, blank=True)
    data_contratacao = DateField('Data de contratação', default=timezone.now, blank=True)
    demitido = BooleanField(default=False, blank=True)
    ultima_mudanca = DateField('Última mudança', auto_now=True, blank=True)
    
    def __str__(self):
        return self.nome
    
    @mark_safe
    def icon(self):
        return f'<a href="/media/{self.foto}" target="_blank"><img src="/media/{self.foto}" style="width: 35px; height: 25px;"></a>'


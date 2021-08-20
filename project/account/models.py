from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, DO_NOTHING, DecimalField, DateField, BooleanField)
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from django.utils import timezone

class User(AbstractUser):
    idade = PositiveIntegerField(blank=True, null=True)
    foto = ImageField('Foto de perfil', upload_to='images/%Y/%m/%d/%M/%f', blank=True, default='images/default.jpg', null=True)
    telefone_pessoal = CharField('Telefone pessoal', max_length=20, blank=True, null=True)
    telefone_comercial = CharField('Telefone de trabalho', max_length=25, blank=True, null=True)
    cpf = CharField('CPF', max_length=25, blank=True, null=True)
    empresario = BooleanField(default=False, blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    @mark_safe
    def icon(self):
        return f'<a href="/media/{self.foto}" target="_blank"><img src="/media/{self.foto}" style="width: 35px; height: 25px;"></a>'


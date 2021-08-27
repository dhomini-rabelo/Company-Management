from django.forms import ModelForm, ValidationError
from .models import *


class EmpresaForm(ModelForm):
    class Meta:
      exclude = 'presidente', 'funcionarios', 'link', 'despesas'
      model = Empresa
      

class GestorForm(ModelForm):
    class Meta:
      exclude = 'nome', 'foto', 'email', 'demitido'
      model = Funcionario

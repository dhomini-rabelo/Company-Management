from django.forms import ModelForm, ValidationError
from .models import *


class EmpresaForm(ModelForm):
    class Meta:
      exclude = 'presidente', 'funcionarios', 'link', 'despesas'
      model = Empresa
      

class FuncionarioForm(ModelForm):
    class Meta:
      exclude = 'codigo', 'demitido'
      model = Funcionario

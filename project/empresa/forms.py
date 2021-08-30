from django.forms import ModelForm, ValidationError
from .models import Empresa, Funcionario, Solicitacao, Image


class EmpresaForm(ModelForm):
    class Meta:
      exclude = 'presidente', 'funcionarios', 'link', 'despesas'
      model = Empresa
      

class GestorForm(ModelForm):
    class Meta:
      exclude = 'nome', 'foto', 'email', 'demitido', 'codigo'
      model = Funcionario


class FuncionarioForm(ModelForm):
    class Meta:
      exclude = 'codigo', 'demitido'
      model = Funcionario

class ImageForm(ModelForm):
    class Meta:
      fields = '__all__'
      model = Image
      

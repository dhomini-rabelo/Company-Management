from .django_class import DjangoBase
from .editor import Editor
from pathlib import Path
from .support import *
import io


class DjangoApp(DjangoBase):
    def __init__(self, base_path: str, app: str):
        self.base_path = self.adapt_path(base_path)
        self.app = self.adapt_path(app)
        self.path = f'{self.base_path}/{self.app}'
        assert_folder_existence(self.path)
            
    def create_parts_folder(self):
        try: 
            path = f'{self.path}/templates/Parts'
            Path(path).mkdir()
            assert_folder_existence(path)
            response(f'pasta Parts foi criada no app {self.app}')
        except FileExistsError:
            response(f'pasta Parts já existe no app {self.app}')

    def create_templates_folder(self):
        try: 
            Path(f'{self.path}/templates').mkdir()
            response(f'pasta templates foi criada no app {self.app}')
        except FileExistsError:
            response(f'a pasta templates já existe no app {self.app}')
            
    def create_template(self, name_archive: str, extends_archive: str):
        name = self.adapt_htmlname(name_archive)
        extends = self.adapt_htmlname(extends_archive)
        with io.open(f'{self.path}/templates/{name}', 'w', encoding='utf-8') as arc:
            arc.write('{% extends ' +  f"'{extends}'" + ' %}\n')
            response(f'Criando template {name}\n')
            
    def create_tests_folder(self):
        try:
            Path(f'{self.path}/tests').mkdir()
            response(f'pasta tests foi criada  no app {self.app}')
            with io.open(f'{self.path}/tests/__init__.py', 'w', encoding='utf-8') as arc:
                arc.write('# Módulo python')
        except FileExistsError:
            response(f'a pasta tests já existe no app {self.app}')
            
    def create_test_archive(self, test_name: str):
        name = f'test_{self.adapt_pyname(test_name)}'
        with io.open(f'{self.path}/tests/{name}', 'w', encoding='utf-8') as arc:
            arc.write('from django.test import TestCase\n')
            response(f'Criando {name} na pasta tests')
            
    def create_url_archive(self):
        with io.open(f'{self.path}/urls.py', 'w', encoding='utf-8') as arc:
            arc.write('from django.urls import path\nfrom .views import *\n')
            arc.write('\nurlpatterns = [\n\n]')
            response(f'arquivo urls.py criado no app {self.app}')
    
    def create_forms_archive(self):
        with io.open(f'{self.path}/forms.py', 'w', encoding='utf-8') as arc:
            arc.write('from django.forms import ModelForm, ValidationError\n')
            arc.write('from .models import *\n')
            response(f'arquivo forms.py criado no app {self.app}')

    def create_form(self, model_name: str):
        path = f'{self.path}/forms.py'
        assert_file_existence(path)
        with io.open(path, 'a', encoding='utf-8') as arc:
            arc.write(f'\n\nclass Form{model_name}(ModelForm):\n')
            arc.write(f"    class Meta:\n      fields='__all__'\n")
            arc.write(f"        model = {model_name}\n")
            response(f'criando form para {model_name}')
            
    def import_for_model(self):
        editor = Editor(self.path, 'models.py')
        current_import = 'from django.db import models'
        new_import = 'from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, DO_NOTHING, DecimalField, DateField, BooleanField)'
        nr = editor.replace_code(current_import, new_import) # new_reading
        editor.update(nr)
        response(f'import do model foi editado')



            
    
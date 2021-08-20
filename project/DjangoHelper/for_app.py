from main import base_path as bp
from models.app import DjangoApp


app_name = 'empresa'

app = DjangoApp(bp, app_name)


app.create_template('index', 'base')

#* Criar form
# model = 'Model'
# app.create_form(model)
from main import base_path as bp
from models.app import DjangoApp


app_name = 'empresa'

app = DjangoApp(bp, app_name)


#* Criar form
model = 'Funcionario'
app.create_form(model)
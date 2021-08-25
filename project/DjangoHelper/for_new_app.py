from models.eraser import delete_comments_by_folder
from main import base_path as bp
from models.app import DjangoApp

app_name = 'empresa'

app = DjangoApp(bp, app_name)

#* NOVOS ARQUIVOS
# app.create_url_archive()
# app.create_forms_archive()

#* NOVAS PASTAS
# app.create_templates_folder()
# app.create_parts_folder()
# app.create_tests_folder()

#* ESPECÍFICOS
# delete_comments_by_folder(bp, app_name)

#* TESTS
# tests = ['models', 'views', 'forms']
# for test in tests:
#     app.create_test_archive(test)

#* MODELS
# app.import_for_model()


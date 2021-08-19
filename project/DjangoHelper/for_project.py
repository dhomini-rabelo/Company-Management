from main import base_path as bp
from models.eraser import *
from models.project import *
from models.editor import Editor

project_name = 'core'
delete_comments_by_folder(bp, project_name)


#* APÓS CRIAÇÃO

project = DjangoProject(bp, project_name)
project.create_base_folders()

#* mudanças de código
project.adapt_urls_py()
project.adapt_settings()
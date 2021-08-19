from .django_class import DjangoBase
from .editor import Editor
from pathlib import Path
from time import sleep
from .support import *
import io


class DjangoProject(DjangoBase):
    def __init__(self, base_path: str, project: str):
        self.base_path = self.adapt_path(base_path)
        self.project = self.adapt_path(project)
        self.path = f'{self.base_path}/{self.project}'
        assert_folder_existence(self.path)

    def create_base_folders(self):
        base_folders = ['Static', 'Templates', 'Templates/Parts', 'Media', 'Media/images']
        for new_folder in base_folders:
            sleep(0.5)
            Path(f'{self.base_path}/{new_folder}').mkdir()
            
    def adapt_urls_py(self):
        editor = Editor(self.path, 'urls.py')
        nr = editor.insert_code('from django.urls', 'from django.conf import settings \nfrom django.conf.urls.static import static')  # new_reading
        nr = editor.insert_code(']', '\nurlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\nurlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)', nr)
        editor.update(nr)
    
    def settings_replaces(self):
        replaces = [
            ("        'DIRS': [],", "        'DIRS': [Path(BASE_DIR, 'Templates')],"),
            ("LANGUAGE_CODE = 'en-us'", "LANGUAGE_CODE = 'pt-br'"),
            ("TIME_ZONE = 'UTC'", "TIME_ZONE = 'America/Sao_Paulo'"),
            #("", ""),
        ]
        return replaces
        
    def settings_inserts(self):
        inserts = [
            ("STATIC_URL = '/static/'", "STATIC_URL = '/static/' '\nSTATICFILES_DIRS = [Path(BASE_DIR, 'Static')]\nSTATIC_ROOT = Path('static')\n\nMEDIA_ROOT = Path(BASE_DIR,'Media')\nMEDIA_URL = '/media/'\nMESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'\nSESSION_COOKIE_AGE = 60*60*24*7"),
            #("", ""),
        ]
        return inserts
    
    def adapt_settings(self):
        editor = Editor(self.path, 'urls.py')
        changes = self.settings_inserts() + self.settings_replaces()
        for index_, change in enumerate(changes):
            if index_ == 0:
                nr = editor.replace_code(change[0], change[1])
            else:
                nr = editor.replace_code(change[0], change[1], nr)
        if len(changes) > 0:
            editor.update(nr)
                
            

    
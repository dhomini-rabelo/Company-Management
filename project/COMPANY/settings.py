from pathlib import Path
from django.contrib.messages import constants
from decouple import config
import django_on_heroku

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-g_5ne(!jn1%zuy+&h(p(xiki+(ps-k*9n_(06f(7)9j8_jbztj'

DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'project.account.apps.AccountConfig',
    'project.empresa.apps.EmpresaConfig',
    'crispy_forms',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'COMPANY.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(BASE_DIR, 'Templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
            'filtros': 'Templatestags.filtros',
            }
        },
    },
]

WSGI_APPLICATION = 'COMPANY.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = 'http://localhost:8000/login/'

MESSAGE_TAGS = {
    constants.ERROR : 'alert-danger',
    constants.WARNING : 'alert-warning',
    constants.DEBUG : 'alert-info',
    constants.SUCCESS : 'alert-success',
    constants.INFO : 'alert-info',
}

STATIC_URL = '/static/'

STATICFILES_DIRS = [Path(BASE_DIR, 'Static')]
STATIC_ROOT = Path('static')

MEDIA_ROOT = Path(BASE_DIR,'Media')
MEDIA_URL = '/media/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
SESSION_COOKIE_AGE = 60*60*24*7


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'account.User'


django_on_heroku.settings(locals())
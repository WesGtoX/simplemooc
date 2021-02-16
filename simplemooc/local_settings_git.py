# LOCAL SETTINGS
# CHANGE THE NAME TO 'local_settings.py'
import os


DEBUG = True

TEMPLATE_DEBUG = True


# Armazena o diretorio base do projeto '__file__' é referencia para o primeiro diretório simplemooc.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # SQLITE3 SO PRECISA DO NOME NAS CONFIG
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

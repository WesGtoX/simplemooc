# LOCAL SETTINGS
# CHANGE DE NAME TO 'local_settings.py'


DEBUG = True

TEMPLATE_DEBUG = True

import os

# ARMAZENA O DIRETORIO BASE DO PROJETO '__file__' É REFERENCIA PARA O PRIMEIRO DIRETÓRIO simplemooc.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # SQLITE3 SO PRECISA DO NOME NAS CONFIG
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
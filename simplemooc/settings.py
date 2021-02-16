import os
import dj_database_url

from decouple import config

# Armazena o diretorio base do projeto '__file__' é referencia para o primeiro diretório simplemooc.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

TEMPLATE_DEBUG = config('TEMPLATE_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # aplicação 'auth' que vem por padrão.
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # installed apps
    'taggit',
    'storages',
    'django_extensions',
    # my apps
    # 'path' da aplicação (movendo o 'app' para pasta 'simplemooc', pode ser referenciada dessa maneira).
    'simplemooc.core',
    'simplemooc.accounts',
    'simplemooc.courses',
    'simplemooc.forum',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simplemooc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simplemooc.wsgi.application'

# Database

if config('HEROKU', default=False, cast=bool):
    DATABASES = {
        'default': dj_database_url.config()
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # SQLITE3 SO PRECISA DO NOME NAS CONFIG
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }


# Password validation

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

# Internationalization

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

# STATIC_URL = '/static/'

# Os arquivos relacionados a modelo, serão salvos nesse diretório.
MEDIA_ROOT = os.path.join(BASE_DIR, 'simplemooc', 'media')
# Seria a 'url' base para os arquivos estáticos que são feitos uploads pelo usuário.
MEDIA_URL = '/media/'


# E-mails

ADMINS_EMAIL = config('ADMINS', default=None)

if ADMINS_EMAIL is not None:
    ADMINS = [tuple(i.split(',')) for i in ADMINS_EMAIL.split(';')]

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # settings padrão (pode ser retirada)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default=None)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)
EMAIL_PORT = config('EMAIL_PORT', default=None)
EMAIL_FROM_NAME = config('EMAIL_FROM_NAME', default=None)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL = f'{EMAIL_FROM_NAME} <{EMAIL_HOST_USER}>'
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_SUBJECT_PREFIX = '[Simplemooc] '

CONTACT_EMAIL = EMAIL_HOST_USER

# 'Auth' - redireciona para uma determinada 'url' definida quando efetua o login.
# Pode ser definida manualmente, ou usar o 'accounts' já utilizado no template.
LOGIN_URL = 'accounts:login'
# Redireciona para a home.
LOGIN_REDIRECT_URL = 'core:home'
# URL de logout.
LOGOUT_URL = 'accounts:logout'
# Setar o nome da 'app'.'model', com isso o Django vai saber que
# o usuário do sistema é o nosso model e não o padrão do Django.
AUTH_USER_MODEL = 'accounts.User'

# HEROKU SETTINGS

# Change 'default' database configuration with $DATABASE_URL.
# DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = [
#    os.path.join(PROJECT_ROOT, 'static'),
# ]

# Simplified static file serving.

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
# import django_heroku
# django_heroku.settings(locals())


if config('USE_S3', default=False, cast=bool):
    AWS_STORAGE_BUCKET_NAME = config('S3_BUCKET_NAME', default=None)
    AWS_S3_REGION_NAME = config('S3_REGION_NAME', default=None)
    AWS_ACCESS_KEY_ID = config('S3_KEY_ID', default=None)
    AWS_SECRET_ACCESS_KEY = config('S3_SECRET_KEY', default=None)

    # Tell django-storages the domain to use to refer to static files.
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Tell the staticfiles app to use S3Boto3 storage when writing
    # the collected static files (when you run `collectstatic`).
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'

    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

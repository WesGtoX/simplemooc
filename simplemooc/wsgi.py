import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplemooc.settings')

from dj_static import Cling  # noqa
application = Cling(get_wsgi_application())

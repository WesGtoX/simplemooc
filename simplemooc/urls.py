from django.conf.urls import include, url
from django.contrib import admin

from simplemooc.core.views import home
from simplemooc.core.views import contact

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^contato/$', contact, name='contact'),
    
    url(r'^admin/', include(admin.site.urls)),
]

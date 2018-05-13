from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('', include('simplemooc.core.urls',)),
    path('admin/', admin.site.urls),
]


# ^ - começo de uma string
# $ - final de uma string
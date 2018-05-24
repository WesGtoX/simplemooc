from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('', include('simplemooc.core.urls', namespace='core')),
	path('cursos/', include('simplemooc.courses.urls', namespace='courses')),
    path('admin/', admin.site.urls),
]


# ^ - começo de uma string
# $ - final de uma string
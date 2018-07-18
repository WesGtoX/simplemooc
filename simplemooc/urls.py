from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', include('simplemooc.core.urls', namespace='core')),
	path('conta/', include('simplemooc.accounts.urls', namespace='accounts')),
	path('cursos/', include('simplemooc.courses.urls', namespace='courses')),
	path('forum/', include('simplemooc.forum.urls', namespace='forum')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:		# se estiver em debug...
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)	# ...a variável vai receber mais uma chamada de função que recebe primeiro uma configuração de URL...
																					# que depois vai gerar uma 'view', que recebe uma 'url' que vai pegar o diretório base, e conforme o resto...
																					# da 'url' que foi retornado, ele vai buscar o caminho do arquivo.
																					# 'MEDIA_ROOT' será o diretório base para todos os arquivos de média de todos os 'Models'...
																					# O 'upload_to' é o sufixo, assim o caminho final será o 'MEDIA_ROOT' + 'upload_to'.
# ^ - começo de uma string.
# $ - final de uma string.
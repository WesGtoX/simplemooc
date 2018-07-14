from django.contrib import admin

from .models import Thread, Reply


class ThreadAdmin(admin.ModelAdmin):

	list_display = ['title', 'author', 'created', 'modified']
	search_fields = ['title', 'author__email', 'body']


class ReplyAdmin(admin.ModelAdmin):

	list_display = ['author', 'created', 'modified']
	search_fields = ['thread__title', 'author__email', 'reply']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)


# 'author__email', é dessa forma que conseguimos fazer o acesso de um atributo de uma 'ForeignKey', fazemos um filtro com o email do author.
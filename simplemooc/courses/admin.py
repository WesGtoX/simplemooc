from django.contrib import admin

from .models import (Course, Enrollment, Announcement, Comment, Lesson, Material)


class CourseAdmin(admin.ModelAdmin):		# representa as opções do curso de uma forma melhor, com mais opções.
	
	list_display = ['name', 'slug', 'start_date', 'created_at']		# o que será mostrado.
	search_fields = ['name', 'slug']		# campo de busca.
	prepopulated_fields = {'slug': ('name',)}	# preenche automaticamente com a devida formatação o campo 'slug'.


class MaterialInlineAdmin(admin.StackedInline):		# 'InlineModelAdmin', pode ser escolhido duas formas de exibição 'StackedInline' (vertical) e o 'TabularInline' (horizontal).

	model = Material 		# model indicado que será tratado como 'InlineModelAdmin'.


class LessonAdmin(admin.ModelAdmin):

	list_display = ['name', 'number', 'course', 'release_date']		# o que será mostrado.
	search_fields = ['name', 'description']		# campo de busca.
	list_filter = ['created_at']		# filtragem lateral. Cria um campo de filtro lateral no admin.

	inlines = [		# variável 'inlines' que é uma lista.
		MaterialInlineAdmin
	]

admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment, Material])
admin.site.register(Lesson, LessonAdmin)
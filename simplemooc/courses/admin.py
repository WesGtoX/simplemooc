from django.contrib import admin

from .models import Course

class CourseAdmin(admin.ModelAdmin):		# representa as opções do curso de uma forma melhor, com mais opções.
	list_display = ['name', 'slug', 'start_date', 'created_at']
	search_fields = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}	# preenche automaticamente com a devida formatação o campo 'slug'.

admin.site.register(Course, CourseAdmin)
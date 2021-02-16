from django.contrib import admin
from simplemooc.courses.models import (
    Course, Enrollment, Announcement,
    Comment, Lesson, Material
)


class CourseAdmin(admin.ModelAdmin):
    """
    Representa as opções do curso de uma forma melhor, com mais opções.
    """

    # O que será mostrado.
    list_display = ['name', 'slug', 'start_date', 'created_at']
    # Campo de busca.
    search_fields = ['name', 'slug']
    # Via 'javascript', preenche automaticamente com a devida formatação o campo 'slug'.
    prepopulated_fields = {'slug': ('name',)}


class MaterialInlineAdmin(admin.StackedInline):
    """
    'InlineModelAdmin', pode ser escolhido duas formas de exibição:
    'StackedInline' (vertical)
    'TabularInline' (horizontal)

    'model' indicado que será tratado como 'InlineModelAdmin'
    """

    model = Material


class LessonAdmin(admin.ModelAdmin):
    # O que será mostrado.
    list_display = ['name', 'number', 'course', 'release_date']

    # Campo de busca.
    search_fields = ['name', 'description']

    # Filtragem lateral. Cria um campo de filtro lateral no 'admin'.
    list_filter = ['created_at']

    # Variável 'inlines' que é uma lista.
    inlines = [MaterialInlineAdmin]


admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment, Material])
admin.site.register(Lesson, LessonAdmin)

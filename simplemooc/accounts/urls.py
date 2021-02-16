from django.urls import path

# Alterar o nome para evitar conflito de 'views'.
from django.contrib.auth import views as auth_views
from simplemooc.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Ao invés de criar minha própria 'view', estou colocando uma 'view' direto do Django.
    # 3ª Parâmetro que é um dicionário, serve para parâmetros nomeados,
    # que serão passados para essa 'view'. Faz a substituição na 'view'.
    path('entrar/', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),

    # Vai ser redirecionado para a 'view' 'home', da 'app' 'core'.
    path('sair/', auth_views.logout, {'next_page': 'core:home'}, name='logout'),
    path('cadastre-se/', views.register, name='register'),
    path('nova-senha/', views.password_reset, name='password_reset'),
    path('confirmar-nova-senha/<slug:key>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('editar/', views.edit, name='edit'),
    path('editar-senha/', views.edit_password, name='edit_password'),
]

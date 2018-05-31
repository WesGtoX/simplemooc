from django.urls import path
from django.contrib.auth import views as auth_views		# alterar o nome para evitar conflito de 'views'
from . import views

app_name = 'accounts'
urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	
	path('entrar/', auth_views.login,	# ao invés de criar minha própria view, estou colocando uma view direto do Django
		{'template_name': 'accounts/login.html'}, name='login'),	# 3ª Parâmetro que é um dicionário, serve para parâmetros nomeados, que serão passados para essa view. Faz a substituição na view.
	
	path('sair/', auth_views.logout, 
		{'next_page': 'core:home'},	name='logout'),# vai ser redirecionado para a view 'home', da app core
	
	path('cadastre-se/', views.register, name='register'),
]

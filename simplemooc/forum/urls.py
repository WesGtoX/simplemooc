from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
	path('', views.index, name='index'),
	path('tag/<slug:tag>/', views.index, name='index_tagged'),		# duas 'urls' para a mesma 'view'.
	path('<slug:slug>/', views.thread, name='thread'),
]
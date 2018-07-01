from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
	path('', views.index, name='index'),
	#path('<int:pk>/', views.details, name='details'),
	path('<slug:slug>/', views.details, name='details'),
	path('<slug:slug>/inscricao/', views.enrollment, name='enrollment'),
]
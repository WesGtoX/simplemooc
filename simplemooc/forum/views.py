from django.shortcuts import render
from django.views.generic import TemplateView


class ForumView(TemplateName):

	template_name = 'forum/index.html'
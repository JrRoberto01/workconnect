from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(TemplateView, LoginRequiredMixin):

    def get(self, request):
        print('Teste')
        return render(request, 'index.html')
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        user = request.user
        if user:
            return render(request, 'index.html')
        else:
            return redirect('login')
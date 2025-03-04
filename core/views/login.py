from django.views.generic import TemplateView
from django.shortcuts import render, redirect

class LoginTemplateView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        # Verificar se o usuário já está autenticado com JWT
        if request.user.is_authenticated:
            return redirect('index')

        # Se não estiver autenticado, exibe a tela de login
        return super().get(request, *args, **kwargs)

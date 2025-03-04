from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class ChatView(TemplateView):
    template_name = "chat.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')  # Redireciona se o usuário não estiver logado
        return super().dispatch(request, *args, **kwargs)
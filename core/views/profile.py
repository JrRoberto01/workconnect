from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..models import Organizacao


class ProfileView(TemplateView):
    template_name = "profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')  # Redireciona se o usuário não estiver logado

        if not Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
            return redirect('create-organization')

        return super().dispatch(request, *args, **kwargs)
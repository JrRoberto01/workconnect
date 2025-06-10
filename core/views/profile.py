from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from ..models import Organizacao, CustomUser, Post
from django.contrib.auth import get_user_model
User = get_user_model()


class ProfileView(TemplateView):
    template_name = "profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')

        if not Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
            return redirect('create-organization')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_id = self.kwargs.get('user_id')
        
        if user_id:
            usuario = get_object_or_404(User, pk=user_id)
        else:
            usuario = self.request.user

        context['usuario'] = usuario
        context['user'] = usuario  # se o template usa {{ user }}, também já fica funcionando
        context['posts'] = Post.objects.filter(autor=usuario).order_by('-created_at')

        return context
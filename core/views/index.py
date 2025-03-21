from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..models import Organizacao

class IndexView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')  # Redireciona se o usuário não estiver logado

        if not Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
            return redirect('create-organization')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        organization = Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).first()

        context = {
            'organization': organization,
        }
        print(organization)

        return render(request, 'index.html', context)
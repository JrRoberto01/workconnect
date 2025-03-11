from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..models import Organizacao, Grupo
from ..forms import GroupForm

class GroupView(TemplateView):
    template_name = "groups.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')  # Redireciona se o usuário não estiver logado

        if not Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
            return redirect('create-organization')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        organization = Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).first()
        groups = Grupo.objects.filter(deleted_at__isnull=True, membros=request.user)
        add_form = GroupForm()

        context = {
            'organization': organization,
            'groups': groups,
            'add_form': add_form,
        }

        return render(request, 'groups.html', context)

    def post(self, request):
        form = GroupForm(request.POST, request.FILES)

        if form.is_valid():
            group = form.save(user=request.user)
            return redirect('group')

        organization = Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).first()
        groups = Grupo.objects.filter(deleted_at__isnull=True, membros=request.user)

        context = {
            'organization': organization,
            'groups': groups,
            'form': form,  # Retorna o formulário com erros para o template
        }

        return render(request, 'groups.html', context)
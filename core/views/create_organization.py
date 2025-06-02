from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from ..forms import OrganizacaoForm
from ..models import Organizacao

class CreateOrgView(CreateView):
    model = Organizacao
    form_class = OrganizacaoForm
    template_name = 'create-organization.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return super().form_valid(form)

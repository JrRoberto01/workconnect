from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from ..models import Evento, Organizacao, CustomUser as User
from ..forms import EventoForm

class AgendaView(TemplateView):
    template_name = "agenda.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')

        if not Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
            return redirect('create-organization')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        organization = Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).first()
        eventos = Evento.objects.filter(deleted_at__isnull=True, participantes=request.user).order_by('data')

        print(eventos)
        if organization:
            users = organization.membros.all()
        else:
            users = User.objects.none()

        context['eventos'] = eventos
        context['users'] = users
        context['form'] = EventoForm(user=request.user)

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        evento_id = request.POST.get('evento_id')

        if evento_id:
            #Edição de evento
            evento = get_object_or_404(Evento, id=evento_id)

            if evento.autor != request.user:
                return HttpResponseForbidden("Sem permissão pra editar.")

            form = EventoForm(request.POST, instance=evento, user=request.user)
            if form.is_valid():
                evento = form.save(commit=False)
                evento.save()
                participantes_ids = request.POST.getlist('participantes')
                evento.participantes.set(participantes_ids)
                print('Evento atualizado')
                return redirect('agenda_view')
            else:
                context = self.get_context_data()
                context['form'] = form
                print('Evento Quebrou')
                return self.render_to_response(context)
        else:
            #Criação de Evento
            form = EventoForm(request.POST, user=request.user)
            if form.is_valid():
                evento = form.save(commit=False)
                evento.autor = request.user
                evento.save()

                participantes_ids_from_form = [int(p_id) for p_id in request.POST.getlist('participantes') if p_id.isdigit()]

                if request.user.id not in participantes_ids_from_form:
                    participantes_ids_from_form.append(request.user.id)

                evento.participantes.set(participantes_ids_from_form)

                messages.success(request, "Evento criado com sucesso!")
                return redirect('agenda_view')
            else:
                context = self.get_context_data()
                context['form'] = form
                return self.render_to_response(context)


@login_required
def deletar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if evento.autor != request.user:
        return HttpResponseForbidden("Você não pode deletar esse evento.")

    if request.method == "POST":
        evento.deleted_at = timezone.now()
        evento.save()
        messages.success(request, "Evento excluído com sucesso!")
        return redirect('agenda_view')

    return redirect('agenda_view')

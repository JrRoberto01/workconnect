from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Evento, Organizacao, CustomUser as User
from ..forms import EventoForm

@login_required
def agenda_view(request):
    organization = Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).first()
    eventos = Evento.objects.filter(deleted_at__isnull=True, participantes=request.user).order_by('data')
    users = User.objects.filter(membros_organizacao__id = organization.id)

    if request.method == 'POST':
        evento_id = request.POST.get('evento_id')
        if evento_id:
            # Edição
            evento = get_object_or_404(Evento, id=evento_id)
            if evento.autor != request.user:
                return HttpResponseForbidden("Sem permissão pra editar.")

            form = EventoForm(request.POST, instance=evento)
            if form.is_valid():
                evento = form.save(commit=False)
                evento.save()
                participantes_ids = request.POST.getlist('participantes')
                evento.participantes.set(participantes_ids)
                return redirect('agenda_view')
        else:
            # Criação
            form = EventoForm(request.POST)
            if form.is_valid():
                evento = form.save(commit=False)
                evento.autor = request.user
                evento.save()
                form.save_m2m()
                return redirect('agenda_view')
    else:
        form = EventoForm()

    return render(request, 'agenda.html', {'eventos': eventos, 'form': form, 'users': users})

@login_required
def deletar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if evento.autor != request.user:
        return HttpResponseForbidden("Você não pode deletar esse evento.")

    if request.method == "POST":
        evento.delete()
        messages.success(request, "Evento excluído com sucesso!")
        return redirect('agenda_view')
    
    return redirect('agenda_view')

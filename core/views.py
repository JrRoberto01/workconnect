from django.shortcuts import render
from django.http import JsonResponse
from .tasks import soma_numeros
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View

def trigger_task(request):
    # Dispara a tarefa de forma assíncrona
    task = soma_numeros.delay(3, 4)
    return JsonResponse({
        'message': 'Tarefa disparada!',
        'task_id': task.id
    })

class IndexView(TemplateView):
    def get(self, request):
        print('Teste')
        return render(request, 'index.html')
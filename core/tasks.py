from celery import shared_task
import time

@shared_task
def soma_numeros(a, b):
    """Esta tarefa simula um processamento demorado e retorna a soma de dois números."""
    time.sleep(5)  # Simula uma demora de 5 segundos
    return a + b
import os
from celery import Celery

# Define o módulo de configurações do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workconnect.settings')

# Cria a instância do Celery
app = Celery('workconnect')

# Carrega as configurações do Django com namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente as tarefas em cada app do Django
app.autodiscover_tasks()
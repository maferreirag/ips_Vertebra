import os
from celery import Celery

# Establecer la configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ips.settings')

# Crea una instancia de la aplicación Celery
app = Celery('ips')

# Configuración de Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Busca tareas de Celery en las aplicaciones Django
app.autodiscover_tasks()
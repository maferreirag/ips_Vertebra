# librería de procesamiento gráfico: pillow (fork de PIL) [probé a usar OpenCV pero la descarté por engorrosa]
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Imagen, HistorialProcesamiento, RegistroError
import json
from django.http import JsonResponse
import redis
from PIL import Image, ImageOps
from celery import Celery


# Configuración de Redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# Configuración de Celery (ips por: image processing system)
app = Celery('ips', broker='redis://localhost:6379/0')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

def import_postman_collection(request):
    try:
        with open('ips_app/postman/my_collection.json') as file:
            collection = json.load(file)

        # ¡¡¡ ojo: procesar aquí la colección !!!
        
        return JsonResponse({'success': True})
    except FileNotFoundError:
        return JsonResponse({'error': 'Archivo no encontrado'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al procesar el archivo JSON'})

def index(request):
    return HttpResponse('<h1>IPS - Imaging Process System</h1>')

@app.task(bind=True)
def procesar_imagen(self, imagen_id, transformacion):
    proceso_img = None
    if transformacion == 'invertir':
        proceso_img = 'Invertir los colores'
    elif transformacion == 'blanco_negro':
        proceso_img = 'Pasar a Blanco y Negro'
    elif transformacion == 'rotar':
        proceso_img = 'Rotar la imagen 90 grados'
    elif transformacion == 'invertir_eje':
        proceso_img = 'Invertir imagen sobre su eje vertical'

    try:
        imagen = Imagen.objects.get(id=imagen_id)
        img = Image.open(default_storage.open(imagen.archivo.name))

        if transformacion == 'invertir':
            img = img.convert('RGB')
            img = ImageOps.invert(img)
        elif transformacion == 'blanco_negro':
            img = img.convert('L')
        elif transformacion == 'rotar':
            img = img.rotate(90, expand=True)
        elif transformacion == 'invertir_eje':
            img = ImageOps.flip(img)

        # guardar la imagen procesada
        with default_storage.open(imagen.archivo.name, 'wb') as f:
            img.save(f)

        # Registro de historial exitoso
        HistorialProcesamiento.objects.create(imagen=imagen, paso=proceso_img, estado='SUCCESS')

    except ObjectDoesNotExist:
        # Registro de error si la imagen no existe
        RegistroError.objects.create(imagen_id=imagen_id, paso=proceso_img, descripcion='La imagen no existe')
    except Exception as e:
        # Registro de error en caso de excepción
        RegistroError.objects.create(imagen_id=imagen_id, paso=proceso_img, descripcion=str(e))

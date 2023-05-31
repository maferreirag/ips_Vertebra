from django.shortcuts import render
from django.http import HttpResponse
from .tasks import procesar_imagen

def index(request):
    #return HttpResponse("¡Hola, mundo! Esta es la página de inicio de mi aplicación.")
    return render(request, 'ips_app/index.html')

def procesar_imagenes(request):
    if request.method == 'POST':
        # Obtener los datos enviados desde el formulario
        imagen_ids = request.POST.getlist('imagen_id')
        transformaciones = request.POST.getlist('transformacion')

        # Procesar cada imagen en segundo plano
        for imagen_id, transformacion in zip(imagen_ids, transformaciones):
            # Llamar a la tarea de Celery para procesar la imagen
            procesar_imagen.delay(imagen_id, transformacion)

        # Redirigir a una página de confirmación o mostrar un mensaje de éxito
        return redirect('confirmacion')

    # Si no es una solicitud POST, renderizar el formulario HTML
    #return HttpResponse('Mensaje: Error en la solicitud')
    return render(request, 'index.html')



def procesar_imagen(request):
    # Obtener archivos de imagen y transformaciones seleccionadas desde la solicitud

    # Convertir archivos de imagen a rutas de archivo
    imagenes = [imagen.file for imagen in request.FILES.getlist('imagen')]

    # Obtener transformaciones seleccionadas desde la solicitud
    transformaciones = request.POST.getlist('transformacion')

    # Llamar a la tarea de Celery para procesar las imágenes en segundo plano
    procesar_imagenes.delay(imagenes, transformaciones)

    # Redireccionar o devolver una respuesta al usuario

def contact(request):
    return render(request, 'contact.html')
from celery import task
from PIL import Image

@task
def procesar_imagenes(imagenes, transformaciones):
    for imagen_path in imagenes:
        imagen = Image.open(imagen_path)

        for transformacion in transformaciones:
            if transformacion == 'invertir':
                imagen = imagen.transpose(Image.FLIP_LEFT_RIGHT)
            elif transformacion == 'blanco_negro':
                imagen = imagen.convert('L')
            elif transformacion == 'rotar':
                imagen = imagen.rotate(90)
            elif transformacion == 'invertir_eje':
                imagen = imagen.transpose(Image.FLIP_TOP_BOTTOM)

        # Guardar la imagen procesada
        imagen.save('ruta/destino/' + imagen_path.name)
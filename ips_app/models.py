from django.db import models

# tabla para almacenar información de la imagenes procesadas
class Imagen(models.Model):
    nombre = models.CharField(max_length=100)
    archivo = models.ImageField(upload_to='images/')

# tabla para registrar el proceso
class HistorialProcesamiento(models.Model):
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)
    paso = models.CharField(max_length=100)
    estado = models.CharField(max_length=20)
    tiempo_inicio = models.DateTimeField()
    tiempo_fin = models.DateTimeField()
    duracion = models.DateTimeField()

# tabla para registrar los errores que sucedan
class RegistroError(models.Model):
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)
    paso = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

from django.urls import path
from . import views

app_name = 'ips_app'

urlpatterns = [
    #path('templates/', views.index, name='index'),
    path('', views.index, name='index'),
    # demás rutas específicas de la aplicación
]

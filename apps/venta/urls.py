from django.conf.urls import url
from django.urls import path
from . import views
from apps.venta.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Venta'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('nuevo', login_required(views.nuevo), name='nuevo'),
    path('get_producto', login_required(views.get_producto), name='get_producto'),
    path('crear', login_required(views.crear), name='crear'),
    path('editar/<int:id>', views.editar, name='editar'),
    path('editar_save', views.editar_save, name='editar_save'),
    path('get_detalle', login_required(views.get_detalle), name='get_detalle'),
    path('estado', login_required(views.estado), name='estado'),
    path('eliminar', login_required(views.eliminar), name='eliminar'),
    path('chart', login_required(views.grap), name='chart'),
    path('data', login_required(views.data), name='data'),
    #path('editar/<int:id_alumno>', login_required(views.editar), name='editar'),

]

from django.conf.urls import url
from django.urls import path
from . import views
from apps.produccion.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Produccion'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('nuevo', login_required(views.nuevo), name='nuevo'),
    # # path('crear', login_required(views.crear), name='crear'),
    # path('pago_jornada/<int:id>', views.pago_jornada, name='pago_jornada'),
    # path('save_pago', views.save_pago, name='save_pago'),
    # # path('editar_save', views.editar_save, name='editar_save'),
    path('get_detalle', login_required(views.get_detalle), name='get_detalle'),
    # path('get_labor', login_required(views.get_labor), name='get_labor'),
    path('save', login_required(views.save), name='save'),
    # # path('estado', login_required(views.estado), name='estado'),
    # # path('eliminar', login_required(views.eliminar), name='eliminar'),
    # #path('editar/<int:id_alumno>', login_required(views.editar), name='editar'),

]

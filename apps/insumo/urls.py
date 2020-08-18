from django.conf.urls import url
from django.urls import path
from . import views
from apps.cliente.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Insumos'

urlpatterns = [
    path('lista', login_required(views.lista), name='lista'),
    path('nuevo', login_required(views.nuevo), name='nuevo'),
    path('crear', login_required(views.crear), name='crear'),
    path('ajax', login_required(views.ajax), name='ajax'),
    #path('inventario', login_required(views.stock), name='inventario'),
    #path('editar/<int:id_alumno>', login_required(views.editar), name='editar'),

]

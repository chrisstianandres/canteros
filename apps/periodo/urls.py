from django.conf.urls import url
from django.urls import path
from . import views
from apps.periodo.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Clientes'

urlpatterns = [
    path('lista', login_required(views.lista), name='lista'),
    path('nuevo', login_required(views.nuevo), name='nuevo'),
    path('crear', login_required(views.crear), name='crear'),
    path('estado', login_required(views.estado), name='estado'),
    path('check', login_required(views.check), name='check'),
    path('editar/<int:id>', login_required(views.editar), name='editar'),

]

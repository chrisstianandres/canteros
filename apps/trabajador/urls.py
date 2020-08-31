from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'Trabajador'

urlpatterns = [
    path('lista', login_required(views.lista), name='lista'),
    path('nuevo', login_required(views.nuevo), name='nuevo'),
    path('crear', login_required(views.crear), name='crear'),
    path('editar/<int:id>', login_required(views.editar), name='editar'),
    path('estado', login_required(views.estado), name='estado'),

]

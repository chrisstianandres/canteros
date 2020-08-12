import json

from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.trabajador.forms import TrabajadorForm
from apps.trabajador.models import Trabajador

opc_icono = 'fab fa-pied-piper-alt'
opc_entidad = 'Trabajador'
crud = '/trabajador/crear'


def lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nuevo Trabajador', 'titulo': 'Listado de Trabajador',
        'nuevo': '/trabajador/nuevo'
    }
    list = Trabajador.objects.all()
    data['list'] = list
    return render(request, "front-end/trabajador/trabajador_list.html", data)

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Trabajador', 'action': 'add', 'titulo': 'Nuevo Registro de un Trabajador',
    }
    if request.method == 'GET':
        data['form'] = TrabajadorForm()
    return render(request, 'front-end/trabajador/trabajador_form.html', data)

def crear(request):
    f = TrabajadorForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Trabajador', 'action': 'add', 'titulo': 'Nuevo Registro de un Trabajador'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = TrabajadorForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/trabajador/trabajador_form.html', data)
            return HttpResponseRedirect('/trabajador/lista')

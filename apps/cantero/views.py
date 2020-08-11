from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponse
from apps.cantero.forms import CanteroForm
from apps.cantero.models import Cantero
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

opc_icono = 'fa fa-tractor'
opc_entidad = 'Canteros'
crud = '/cantero/crear'


def lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nuevo Cantero', 'titulo': 'Listado de Cantero',
        'nuevo': '/cantero/nuevo'
    }
    list = Cantero.objects.all()
    data['list'] = list
    return render(request, "front-end/cantero/cantero_list.html", data)

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Cantero', 'action': 'add', 'titulo': 'Nuevo Registro de un Cantero',
    }
    if request.method == 'GET':
        data['form'] = CanteroForm()
    return render(request, 'front-end/cantero/cantero_form.html', data)

def crear(request):
    f = CanteroForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Cantero', 'action': 'add', 'titulo': 'Nuevo Registro de un Cantero'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = CanteroForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/cantero/cantero_form.html', data)
            return HttpResponseRedirect('/cantero/lista')

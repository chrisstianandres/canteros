from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponse
from apps.insumo.forms import InsumoForm
from apps.insumo.models import Insumo
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

opc_icono = 'fa fa-tags'
opc_entidad = 'Insumos'
crud = '/insumo/crear'


def lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nuevo Insumo', 'titulo': 'Listado de Insumos',
        'nuevo': '/insumo/nuevo'
    }
    list = Insumo.objects.all()
    data['list'] = list
    return render(request, "front-end/insumo/insumo_list.html", data)

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Insumo', 'action': 'add', 'titulo': 'Nuevo Registro de un Insumo',
    }
    if request.method == 'GET':
        data['form'] = InsumoForm()
    return render(request, 'front-end/insumo/insumo_form.html', data)

def crear(request):
    f = InsumoForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Insumo', 'action': 'add', 'titulo': 'Nuevo Registro de un Insumo'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = InsumoForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/insumo/insumo_form.html', data)
            return HttpResponseRedirect('/insumo/lista')

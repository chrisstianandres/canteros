from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponse
from apps.cliente.forms import ClienteForm
from apps.cliente.models import Cliente
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

opc_icono = 'fa fa-user'
opc_entidad = 'Clientes'
crud = '/cliente/crear'


def cliente_lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nuevo Cliente', 'titulo': 'Listado de Clientes',
        'nuevo': '/cliente/nuevo'
    }
    list = Cliente.objects.all()
    data['list'] = list
    return render(request, "front-end/cliente/cliente_list.html", data)

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Cliente', 'action': 'add', 'titulo': 'Nuevo Registro de un Cliente',
    }
    if request.method == 'GET':
        data['form'] = ClienteForm()
    return render(request, 'front-end/cliente/cliente_form.html', data)

def crear(request):
    f = ClienteForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Cliente', 'action': 'add', 'titulo': 'Nuevo Registro de un Cliente'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = ClienteForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/cliente/cliente_form.html', data)
            return HttpResponseRedirect('/cliente/lista')

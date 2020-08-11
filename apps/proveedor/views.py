from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponse
from apps.proveedor.forms import ProveedorForm
from apps.proveedor.models import Proveedor
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

opc_icono = 'fa fa-truck'
opc_entidad = 'Proveedor'
crud = '/proveedor/crear'


def proveedor_lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nuevo Proveedor', 'titulo': 'Listado de Proveedor',
        'nuevo': '/proveedor/nuevo'
    }
    list = Proveedor.objects.all()
    data['list'] = list
    return render(request, "front-end/proveedor/proveedor_list.html", data)

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Proveedor', 'action': 'add', 'titulo': 'Nuevo Registro de un Proveedor',
    }
    if request.method == 'GET':
        data['form'] = ProveedorForm()
    return render(request, 'front-end/proveedor/proveedor_form.html', data)

def crear(request):
    f = ProveedorForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Proveedor', 'action': 'add', 'titulo': 'Nuevo Registro de un Proveedor'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = ProveedorForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/proveedor/proveedor_form.html', data)
            return HttpResponseRedirect('/proveedor/lista')

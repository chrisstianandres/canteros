from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponse
from apps.configuracion.forms import EmpresaForm
from apps.configuracion.models import Empresa
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

from apps.configuracion.models import Empresa

opc_icono = 'fa fa-cogs'
opc_entidad = 'Configuracion'
crud = '/cantero/editar'


def editar(request):
    config = Empresa.objects.get(id=1)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad,
        'boton': 'Editar', 'titulo': 'Configuracion', 'form': EmpresaForm(instance=config)
    }
    if request.method == 'GET':
        f = EmpresaForm(instance=config)
    else:
        f = EmpresaForm(request.POST, instance=config)
        if f.is_valid():
            f.save()
            data['form'] = f
        else:
            data['form'] = f
        return render(request, 'front-end/empresa/empresa_form.html', data)
    data['form'] = f
    return render(request, 'front-end/empresa/empresa_form.html', data)


def nuevo(request):
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad,
        'boton': 'Editar', 'titulo': 'Configuracion', 'form': EmpresaForm(instance=Empresa.objects.get(id=1))
    }
    return render(request, 'front-end/empresa/empresa_form.html', data)


# def crear(request):
#     f = CanteroForm(request.POST)
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
#         'boton': 'Guardar Cantero', 'action': 'add', 'titulo': 'Nuevo Registro de un Cantero'
#     }
#     action = request.POST['action']
#     data['action'] = action
#     if request.method == 'POST' and 'action' in request.POST:
#         if action == 'add':
#             f = CanteroForm(request.POST)
#             if f.is_valid():
#                 f.save()
#             else:
#                 data['form'] = f
#                 return render(request, 'front-end/cantero/cantero_form.html', data)
#             return HttpResponseRedirect('/cantero/lista')

from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponse
from apps.periodo.forms import PeriodoForm
from apps.periodo.models import Periodo
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

opc_icono = 'far fa-clock'
opc_entidad = 'Periodo'
crud = '/periodo/crear'


def lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nuevo Periodo', 'titulo': 'Listado de Periodos',
        'nuevo': '/periodo/nuevo'
    }
    list = Periodo.objects.all()
    data['list'] = list
    return render(request, "front-end/periodo/periodo_list.html", data)

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Periodo', 'action': 'add', 'titulo': 'Nuevo Registro de un Periodo',
    }
    if request.method == 'GET':
        data['form'] = PeriodoForm()
    return render(request, 'front-end/periodo/periodo_form.html', data)

def crear(request):
    f = PeriodoForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Peridodo', 'action': 'add', 'titulo': 'Nuevo Registro de un Peridodo'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = PeriodoForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/periodo/periodo_form.html', data)
            return HttpResponseRedirect('periodo:lista')

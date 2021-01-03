from datetime import datetime

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.http import HttpResponse, JsonResponse
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
            return HttpResponseRedirect('/periodo/lista')


def editar(request, id):
    periodo = Periodo.objects.get(id=id)
    crud = '/periodo/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Periodo',
    }
    if request.method == 'GET':
        form = PeriodoForm(instance=periodo)
        data['form'] = form
    else:
        form = PeriodoForm(request.POST, instance=periodo)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return redirect('/periodo/lista')
    return render(request, 'front-end/periodo/periodo_form.html', data)


@csrf_exempt
def estado(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            if Periodo.objects.filter(estado=1).exists():
                ps = Periodo.objects.get(estado=1)
                ps.estado = 0
                ps.save()
            es = Periodo.objects.get(id=id)
            es.estado = 1
            es.save()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)


@csrf_exempt
def check(request):
    data = {}
    try:
        date = datetime.now().date()
        if Periodo.objects.filter(desde__lte=date, hasta__gte=date).exists():
            p = Periodo.objects.get(desde__lte=date, hasta__gte=date)
            if p.estado == 1:
                pass
            else:
                p.estado = 1
                p.save()
        else:
            data['error'] = 'Por favor Agregue el periodo ' + str(date.year)
        data['resp'] = True

    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)

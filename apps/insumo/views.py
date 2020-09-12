from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.http import HttpResponse, JsonResponse

from apps.compra.models import Compra, Detalle_compra
from apps.insumo.forms import InsumoForm
from apps.insumo.models import Insumo
from django.http import HttpResponseRedirect
import json
from django.db.models import Q, Sum

opc_icono = 'fa fa-tags'
opc_entidad = 'Insumos'
crud = '/insumo/crear'


def lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nuevo Insumo', 'titulo': 'Listado de Insumos',
        'nuevo': '/insumo/nuevo'}
    return render(request, "front-end/insumo/insumo_list.html", data)


@csrf_exempt
def ajax(request):
    data = [[i.id, i.nombre, i.categoria.nombre, i.descripcion, i.presentacion.nombre, format(i.pvp, '.2f'), i.stock, i.id]
            for i in Insumo.objects.all()]
    return HttpResponse(json.dumps(data), content_type="application/json")


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


def editar(request, id):
    insumo = Insumo.objects.get(id=id)
    crud = '/insumo/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Insumo',
    }
    if request.method == 'GET':
        form = InsumoForm(instance=insumo)
        data['form'] = form
    else:
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return redirect('/insumo/lista')
    return render(request, 'front-end/insumo/insumo_form.html', data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = Insumo.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = "!No se puede eliminar este insumo porque esta referenciado en otros procesos!!"
        data['content'] = "Intenta con otro insumo"
    return JsonResponse(data)



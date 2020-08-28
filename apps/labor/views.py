from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.labor.forms import LaborForm
from apps.labor.models import Labor

opc_icono = 'fab fa-phoenix-framework'
opc_entidad = 'Labores'
crud = '/labor/crear'


def lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nueva Labor', 'titulo': 'Listado de Labores',
        'nuevo': '/labor/nuevo'}
    list = Labor.objects.all()
    data['list'] = list
    return render(request, "front-end/labor/labor_list.html", data)


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Labor', 'action': 'add', 'titulo': 'Nuevo Registro de una Labor',
    }
    if request.method == 'GET':
        data['form'] = LaborForm()
    return render(request, 'front-end/labor/labor_form.html', data)


def crear(request):
    f = LaborForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Labor', 'action': 'add', 'titulo': 'Nuevo Registro de una Labor'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = LaborForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/labor/labor_form.html', data)
            return HttpResponseRedirect('/labor/lista')

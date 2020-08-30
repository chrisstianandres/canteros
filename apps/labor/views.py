import goslate
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

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


def editar(request, id):
    labor = Labor.objects.get(id=id)
    crud = '/labor/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de una Labor',
    }
    if request.method == 'GET':
        form = LaborForm(instance=labor)
        data['form'] = form
    else:
        form = LaborForm(request.POST, instance=labor)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return redirect('/labor/lista')
    return render(request, 'front-end/labor/labor_form.html', data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = Labor.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        gs = goslate.Goslate()
        data['error'] = gs.translate(str(e), 'es')
    return JsonResponse(data)

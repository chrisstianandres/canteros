import goslate
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

from apps.producto.forms import ProductoForm
from apps.producto.models import Producto

opc_icono = 'fa fa-leaf'
opc_entidad = 'Productos'
crud = '/producto/crear'


class lista(ListView):
    model = Producto
    template_name = 'front-end/producto/producto_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Producto'
        data['titulo'] = 'Listado de Productos'
        data['nuevo'] = '/producto/nuevo'
        return data


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Producto', 'action': 'add', 'titulo': 'Nuevo Registro de un Producto',
    }
    if request.method == 'GET':
        data['form'] = ProductoForm()
    return render(request, 'front-end/producto/producto_form.html', data)


def crear(request):
    f = ProductoForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Producto', 'action': 'add', 'titulo': 'Nuevo Registro de un Producto'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = ProductoForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/producto/producto_form.html', data)
            return HttpResponseRedirect('/producto/lista')


def editar(request, id):
    producto = Producto.objects.get(id=id)
    crud = '/producto/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Producto',
    }
    if request.method == 'GET':
        form = ProductoForm(instance=producto)
        data['form'] = form
    else:
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return redirect('/producto/lista')
    return render(request, 'front-end/producto/producto_form.html', data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = Producto.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = "!No se puede eliminar este producto porque esta referenciado en otros procesos!!"
        data['content'] = "Intenta con otro producto"
    return JsonResponse(data)


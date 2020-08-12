from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import *
from apps.categoria.forms import CategoriaForm
from apps.categoria.models import Categoria

opc_icono = 'fas fa-boxes'
opc_entidad = 'Categoria'
crud = '/categoria/crear'

class lista(ListView):
    model = Categoria
    template_name = 'front-end/categoria/categoria_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Categoria'
        data['titulo'] = 'Listado de Categorias'
        data['nuevo'] = '/categoria/nuevo'
        return data

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Categoria', 'action': 'add', 'titulo': 'Nuevo Registro de una Categoria',
    }
    if request.method == 'GET':
        data['form'] = CategoriaForm()
    return render(request, 'front-end/categoria/categoria_form.html', data)

def crear(request):
    f = CategoriaForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Categoria', 'action': 'add', 'titulo': 'Nuevo Registro de una Categoria'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = CategoriaForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/categoria/categoria_form.html', data)
            return HttpResponseRedirect('/categoria/lista')

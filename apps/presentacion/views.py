from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import *
from apps.presentacion.forms import PresentacionForm
from apps.presentacion.models import Presentacion

opc_icono = 'fas fa-box-open'
opc_entidad = 'Presentacion'
crud = '/presentacion/crear'

class lista(ListView):
    model = Presentacion
    template_name = 'front-end/presentacion/presentacion_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Presentacion'
        data['titulo'] = 'Listado de Presentaciones'
        data['nuevo'] = '/presentacion/nuevo'
        return data

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Presentacion', 'action': 'add', 'titulo': 'Nuevo Registro de una Presentacion',
    }
    if request.method == 'GET':
        data['form'] = PresentacionForm()
    return render(request, 'front-end/presentacion/presentacion_form.html', data)

def crear(request):
    f = PresentacionForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Presentacion', 'action': 'add', 'titulo': 'Nuevo Registro de una Presentacion'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = PresentacionForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/presentacion/presentacion_form.html', data)
            return HttpResponseRedirect('/presentacion/lista')

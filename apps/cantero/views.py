from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponse
from apps.cantero.forms import CanteroForm
from apps.cantero.models import Cantero
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

opc_icono = 'fa fa-tractor'
opc_entidad = 'Canteros'
crud = '/cantero/crear'

class lista(ListView):
    model = Cantero
    template_name = 'front-end/cantero/cantero_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Cantero'
        data['titulo'] = 'Listado de Canteros'
        data['nuevo'] = '/cantero/nuevo'
        return data

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Cantero', 'action': 'add', 'titulo': 'Nuevo Registro de un Cantero',
    }
    if request.method == 'GET':
        data['form'] = CanteroForm()
    return render(request, 'front-end/cantero/cantero_form.html', data)

def crear(request):
    f = CanteroForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Cantero', 'action': 'add', 'titulo': 'Nuevo Registro de un Cantero'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = CanteroForm(request.POST)
            if f.is_valid():
                f.save()
            else:
                data['form'] = f
                return render(request, 'front-end/cantero/cantero_form.html', data)
            return HttpResponseRedirect('/cantero/lista')

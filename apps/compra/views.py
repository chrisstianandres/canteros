from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import *
from apps.compra.forms import CompraForm, Detalle_CompraForm
from apps.compra.models import Compra

opc_icono = 'fa fa-tractor'
opc_entidad = 'Compras'
crud = '/compra/crear'


class lista(ListView):
    model = Compra
    template_name = 'front-end/compra/compra_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Compra'
        data['titulo'] = 'Listado de Compras'
        data['nuevo'] = '/compra/nuevo'
        return data

def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Compra', 'action': 'add', 'titulo': 'Nuevo Registro de una Compra',
    }
    if request.method == 'GET':
        data['form'] = CompraForm()
        data['form2'] = Detalle_CompraForm()
    return render(request, 'front-end/compra/compra_form.html', data)
#
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

import json
from datetime import date, datetime
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.cantero.models import Cantero
from apps.produccion.forms import ProduccionForm
from apps.produccion.models import Produccion
from apps.periodo.models import Periodo
from apps.producto.models import Producto

opc_icono = 'fas fa-spa'
opc_entidad = 'Produccion'
crud = '/produccion/crear'


class lista(ListView):
    model = Produccion
    template_name = 'front-end/produccion/produccion_list.html'

    def get_queryset(self):
        queryset = Cantero.objects.order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Ingreso de Produccion'
        data['titulo'] = 'Listado Ingresos de produccion'
        data['nuevo'] = '/produccion/nuevo'
        data['object_list'] = self.get_queryset()
        return data


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Guardar Ingreso', 'action': 'add', 'titulo': 'Nuevo Ingreso de Produccion',
        'key': ''
    }
    if request.method == 'GET':
        data['form'] = ProduccionForm()
        data['list'] = Cantero.objects.filter(estado=0).order_by('id')
        # data['detalle'] = json.dumps(get_detalle_productos())
    return render(request, 'front-end/produccion/produccion_form.html', data)


# def days_between(d1, d2):
#     return abs(d2 - d1).days
#
#
# def get_detalle_productos():
#     data = []
#     try:
#         for i in Trabajador.objects.all().order_by('id'):
#             item = i.toJSON()
#             item['labor'] = json.dumps(get_detalle_labor())
#             item['desde'] = ''
#             item['hasta'] = ''
#             data.append(item)
#     except:
#         pass
#     return data
#
#
# def get_detalle_labor():
#     data = []
#     try:
#         for i in Labor.objects.all().order_by('id'):
#             item = i.toJSON()
#             data.append(item)
#     except:
#         pass
#     return data
#
#
@csrf_exempt
def get_detalle(request):
    data = {}
    try:
        id = request.POST['id']

        if id:
            data = []
            for p in Produccion.objects.filter(cantero_id=id):
                items = p.toJSON()
                data.append(items)
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


#
#
# @csrf_exempt
# def get_labor(request):
#     data = {}
#     try:
#         trabajador = Trabajador.objects.filter(estado=1)
#         data = []
#         for i in trabajador:
#             item = i.toJSON()
#             item['labor'] = ''
#             item['tiempo'] = ''
#             data.append(item)
#     except Exception as e:
#         data['error'] = 'Ha ocurrido un error'
#     return JsonResponse(data, safe=False)
#
#
@csrf_exempt
def save(request):
    data = {}
    if request.method == 'POST':
        datos = json.loads(request.POST['ingresos'])
        if datos:
            with transaction.atomic():
                for i in datos['canteros']:
                    dv = Produccion()
                    dv.fecha = datos['fecha']
                    dv.periodo_id = datos['periodo']
                    dv.cantero_id = i['cantero']
                    dv.producto_id = i['producto']
                    dv.cantidad = int(i['cantidad'])
                    dv.save()
                    x = Producto.objects.get(pk=i['producto'])
                    x.stock = x.stock + int(i['cantidad'])
                    x.save()
                    data['resp'] = True
        else:
            data['resp'] = False
            data['error'] = "Datos Incompletos"
    return HttpResponse(json.dumps(data), content_type="application/json")
#
#
# def pago_jornada(request, id):
#     jornada = Asig_labor.objects.get(id=id)
#     opc_edit = '/asig_labor/save_pago'
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': opc_edit,
#         'boton': 'Guardar Pago', 'titulo': 'Pago de jornada', 'id': id
#     }
#     if request.method == 'GET':
#         form = Asig_LaborForm_pag(instance=jornada)
#         data['form'] = form
#     return render(request, 'front-end/asig_labor/asig_labor_form_pago.html', data)
#
#
# @csrf_exempt
# def save_pago(request):
#     data = {}
#     if request.method == 'POST':
#         datos = json.loads(request.POST['valores'])
#         if datos:
#             with transaction.atomic():
#                 dv = Asig_labor.objects.get(pk=datos['id'])
#                 dv.valor_pag = float(dv.valor_pag) + float(datos['valor_pag'])
#                 dv.saldo = float(dv.saldo) - float(datos['valor_pag'])
#                 dv.save()
#                 hp = Pago()
#                 hp.fecha= datetime.now()
#                 hp.asignacion_id = dv.id
#                 hp.user_id = request.user.id
#                 hp.save()
#                 if dv.saldo == 0.0:
#                     dv.estado = 1
#                     dv.save()
#                 data['resp'] = True
#         else:
#             data['resp'] = False
#             data['error'] = "Datos Incompletos"
#     return HttpResponse(json.dumps(data), content_type="application/json")

import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.asignar_labor.forms import Asig_LaborForm
from apps.asignar_labor.models import Asig_labor
from apps.labor.models import Labor
from apps.trabajador.models import Trabajador
from apps.periodo.models import Periodo

opc_icono = 'fa fa-shopping-bag'
opc_entidad = 'Asignacion de Labores'
crud = '/asig_labor/crear'


class lista(ListView):
    model = Asig_labor
    template_name = 'front-end/asig_labor/asig_labor_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Asignacion de Labores'
        data['titulo'] = 'Listado de Asignacion de Labores'
        data['nuevo'] = '/asig_labor/nuevo'
        return data


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Guardar Asignacion', 'action': 'add', 'titulo': 'Nuevo Registro de una Asignacion',
        'key': ''
    }
    if request.method == 'GET':
        data['form'] = Asig_LaborForm()
        data['list'] = Trabajador.objects.all().order_by('-id')
        data['detalle'] = json.dumps(get_detalle_productos())
    return render(request, 'front-end/asig_labor/asig_labor_form.html', data)


def get_detalle_productos():
    data = []
    try:
        for i in Trabajador.objects.all().order_by('id'):
            item = i.toJSON()
            item['labor'] = json.dumps(get_detalle_labor())
            item['desde'] = ''
            item['hasta'] = ''
            data.append(item)
    except:
        pass
    return data


def get_detalle_labor():
    data = []
    try:
        for i in Labor.objects.all().order_by('id'):
            item = i.toJSON()
            data.append(item)
    except:
        pass
    return data


# @csrf_exempt
# def crear(request):
#     data = {}
#     if request.method == 'POST':
#         datos = json.loads(request.POST['asignar'])
#         if datos:
#             with transaction.atomic():
#                 c = Asig_labor()
#                 c.fecha_asig = datos['fecha_asig']
#                 c.periodo_id = datos['periodo']
#                 c.cantero_id = datos['cantero']
#                 c.save()
#                 for i in datos['insumos']:
#                     dv = Detalle_asig_insumo()
#                     dv.asig_insumo_id = c.id
#                     dv.insumo_id = i['id']
#                     dv.cantidad = int(i['cantidad'])
#                     print(i['cantidad'])
#                     dv.save()
#                     x = Insumo.objects.get(pk=i['id'])
#                     x.stock = x.stock - int(i['cantidad'])
#                     x.save()
#                     data['resp'] = True
#         else:
#             data['resp'] = False
#             data['error'] = "Datos Incompletos"
#     return HttpResponse(json.dumps(data), content_type="application/json")
#
#
# def editar(request, id):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../../asig_insumo/get_insumo',
#         'boton': 'Editar Asignacion de Insumos', 'action': 'edit', 'titulo': 'Editar Registro de una Asignacion',
#         'key': id
#     }
#     asig_insumo = Asig_insumo.objects.get(id=id)
#     if request.method == 'GET':
#         data['form'] = Asig_InsumoForm(instance=asig_insumo)
#         data['form2'] = Detalle_asig_insumo()
#         data['detalle'] = json.dumps(get_detalle_productos(id))
#     return render(request, 'front-end/asig_insumo/asig_insumo_form.html', data)
#
#
# @csrf_exempt
# def editar_save(request):
#     data = {}
#     datos = json.loads(request.POST['asignar'])
#     if request.POST['action'] == 'edit':
#
#         with transaction.atomic():
#             # c = Compra.objects.get(pk=self.get_object().id)
#             c = Asig_insumo.objects.get(pk=request.POST['key'])
#             c.fecha_asig = datos['fecha_asig']
#             c.cantero_id = datos['cantero']
#             c.periodo_id = datos['periodo']
#             c.save()
#             c.detalle_asig_insumo_set.all().delete()
#             for i in datos['insumos']:
#                 dv = Detalle_asig_insumo()
#                 dv.asig_insumo_id = c.id
#                 dv.insumo_id = i['id']
#                 dv.cantidad = int(i['cantidad'])
#                 dv.save()
#                 x = Insumo.objects.get(pk=i['id'])
#                 x.stock = x.stock - int(i['cantidad'])
#                 x.save()
#                 data['resp'] = True
#     else:
#         data['resp'] = False
#         data['error'] = "Datos Incompletos"
#     return HttpResponse(json.dumps(data), content_type="application/json")
#
#
# def get_detalle_productos(id):
#     data = []
#     try:
#         for i in Detalle_asig_insumo.objects.filter(compra_id=id):
#             item = i.insumo.toJSON()
#             item['cantidad'] = i.cantidad
#             data.append(item)
#     except:
#         pass
#     return data
#
#
@csrf_exempt
def get_labor(request):
    data = {}
    try:
        trabajador = Trabajador.objects.filter(estado=1)
        data = []
        for i in trabajador:
            item = i.toJSON()
            item['labor'] = ''
            item['tiempo'] = ''
            data.append(item)
    except Exception as e:
        data['error'] = 'Ha ocurrido un error'
    return JsonResponse(data, safe=False)


# fecha_asig = models.DateField(default=datetime.now)
#    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT)
#    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT)
#    labor = models.ForeignKey(Labor, on_delete=models.CASCADE)
#    desde = models.DateField(default=datetime.now)
#    hasta = models.DateField(default=datetime.now)
@csrf_exempt
def save_asig(request):
    data = {}
    if request.method == 'POST':
        datos = json.loads(request.POST['asignaciones'])
        if datos:
            with transaction.atomic():
                for i in datos['trabajadores']:
                    dv = Asig_labor()
                    dv.fecha_asig = datos['fecha_asig']
                    dv.periodo_id = datos['periodo']
                    dv.trabajador_id = i['trabajador']
                    dv.labor_id = i['labor']
                    dv.desde = i['desde']
                    dv.hasta = i['hasta']
                    dv.save()
                    data['resp'] = True
        else:
            data['resp'] = False
            data['error'] = "Datos Incompletos"
    return HttpResponse(json.dumps(data), content_type="application/json")

# @csrf_exempt
# def get_detalle(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             data = []
#             for p in Detalle_asig_insumo.objects.filter(compra_id=id):
#                 data.append(p.toJSON())
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data, safe=False)


# @csrf_exempt
# def estado(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             es = Compra.objects.get(id=id)
#             es.estado = 0
#             es.save()
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data)
#
#
# @csrf_exempt
# def eliminar(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             es = Compra.objects.get(id=id)
#             es.delete()
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data)

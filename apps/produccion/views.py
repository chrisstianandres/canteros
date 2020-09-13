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


def report(request):
    data = { 'icono': opc_icono, 'entidad': opc_entidad, 'titulo': 'Reporte de Produccion', 'key': ''}
    return render(request, 'front-end/produccion/produccion_report.html', data)


@csrf_exempt
def data(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    try:
        if start_date == '' and end_date == '':
            produccion = Produccion.objects.all()
            for c in produccion:
                data.append([
                    c.id,
                    c.fecha.strftime('%d-%m-%Y'),
                    c.periodo.nombre,
                    c.cantero.nombre,
                    c.producto.nombre,
                    c.producto.categoria.nombre,
                    c.producto.presentacion.nombre,
                    c.cantidad
                ])
        else:
            produccion = Produccion.objects.filter(fecha__range=[start_date, end_date])
            for c in produccion:
                data.append([
                    c.id,
                    c.fecha.strftime('%d-%m-%Y'),
                    c.periodo.nombre,
                    c.cantero.nombre,
                    c.producto.nombre,
                    c.producto.categoria.nombre,
                    c.producto.presentacion.nombre,
                    c.cantidad
                ])
    except:
        pass
    return JsonResponse(data, safe=False)

import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.venta.forms import VentaForm, Detalle_VentaForm
from apps.venta.models import Venta, Detalle_venta
from apps.configuracion.models import Empresa
from apps.producto.models import Producto

opc_icono = 'fa fa-shopping-basket '
opc_entidad = 'Ventas'
crud = '/venta/crear'


class lista(ListView):
    model = Venta
    template_name = 'front-end/venta/venta_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Venta'
        data['titulo'] = 'Listado de Ventas'
        data['nuevo'] = '/venta/nuevo'
        return data


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../venta/get_producto',
        'boton': 'Guardar Venta', 'action': 'add', 'titulo': 'Nuevo Registro de una Venta',
        'key': ''
    }
    if request.method == 'GET':
        data['form'] = VentaForm()
        data['form2'] = Detalle_VentaForm()
        data['detalle'] = []
    return render(request, 'front-end/venta/venta_form.html', data)


@csrf_exempt
def crear(request):
    data = {}
    if request.method == 'POST':
        datos = json.loads(request.POST['ventas'])
        if datos:
            with transaction.atomic():
                c = Venta()
                c.fecha_venta = datos['fecha_venta']
                c.cliente_id = datos['cliente']
                c.subtotal = float(datos['subtotal'])
                c.iva = float(datos['iva'])
                c.total = float(datos['total'])
                c.save()
                for i in datos['productos']:
                    dv = Detalle_venta()
                    dv.venta_id = c.id
                    dv.producto_id = i['id']
                    dv.cantidad = int(i['cantidad'])
                    dv.save()
                    x = Producto.objects.get(pk=i['id'])
                    x.stock = x.stock - int(i['cantidad'])
                    x.save()
                    data['resp'] = True
        else:
            data['resp'] = False
            data['error'] = "Datos Incompletos"
    return HttpResponse(json.dumps(data), content_type="application/json")


def editar(request, id):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../../venta/get_producto',
        'boton': 'Editar Venta', 'action': 'edit', 'titulo': 'Editar Registro de una Venta',
        'key': id
    }
    venta = Venta.objects.get(id=id)
    if request.method == 'GET':
        data['form'] = VentaForm(instance=venta)
        data['form2'] = Detalle_VentaForm()
        data['detalle'] = json.dumps(get_detalle_productos(id))
    return render(request, 'front-end/venta/venta_form.html', data)


@csrf_exempt
def editar_save(request):
    data = {}
    datos = json.loads(request.POST['ventas'])
    if request.POST['action'] == 'edit':

        with transaction.atomic():
            # c = Compra.objects.get(pk=self.get_object().id)
            c = Venta.objects.get(pk=request.POST['key'])
            c.fecha_venta = datos['fecha_venta']
            c.cliente_id = datos['cliente']
            c.subtotal = float(datos['subtotal'])
            c.iva = float(datos['iva'])
            c.total = float(datos['total'])
            c.save()
            c.detalle_venta_set.all().delete()
            for i in datos['productos']:
                dv = Detalle_venta()
                dv.venta_id = c.id
                dv.producto_id = i['id']
                dv.cantidad = int(i['cantidad'])
                dv.save()
                data['resp'] = True
    else:
        data['resp'] = False
        data['error'] = "Datos Incompletos"
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_detalle_productos(id):
    data = []
    try:
        for i in Detalle_venta.objects.filter(venta_id=id):
            iva_emp = Empresa.objects.get(pk=1)
            item = i.producto.toJSON()
            item['cantidad'] = i.cantidad
            item['iva_emp'] = format(iva_emp.iva, '.2f')
            data.append(item)
    except:
        pass
    return data


@csrf_exempt
def get_producto(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            producto = Producto.objects.filter(pk=id)
            iva_emp = Empresa.objects.get(pk=1)
            data = []
            for i in producto:
                item = i.toJSON()
                item['cantidad'] = 1
                item['subtotal'] = 0.00
                item['iva_emp'] = iva_emp.iva
                data.append(item)
        else:
            data['error'] = 'No ha selecionado ningun Producto'
    except Exception as e:
        data['error'] = 'Ha ocurrido un error'
    return JsonResponse(data, safe=False)


@csrf_exempt
def get_detalle(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            data = []
            for p in Detalle_venta.objects.filter(venta_id=id):
                data.append(p.toJSON())
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


@csrf_exempt
def estado(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            es = Venta.objects.get(id=id)
            es.estado = 0
            es.save()
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            es = Venta.objects.get(id=id)
            es.delete()
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)

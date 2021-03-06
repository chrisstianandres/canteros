import json
from datetime import datetime

from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.compra.forms import CompraForm, Detalle_CompraForm
from apps.compra.models import Compra, Detalle_compra
from apps.configuracion.models import Empresa
from apps.insumo.models import Insumo

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

opc_icono = 'fa fa-shopping-bag'
opc_entidad = 'Compras'
crud = '/compra/crear'


class lista(ListView):
    model = Compra
    template_name = 'front-end/compra/compra_list.html'

    def get_queryset(self):
        return Compra.objects.none()

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
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../compra/get_insumo',
        'boton': 'Guardar Compra', 'action': 'add', 'titulo': 'Nuevo Registro de una Compra',
        'key': ''
    }
    if request.method == 'GET':
        data['form'] = CompraForm()
        data['form2'] = Detalle_CompraForm()
        data['detalle'] = []
    return render(request, 'front-end/compra/compra_form.html', data)


@csrf_exempt
def data(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')

    try:
        if start_date == '' and end_date == '':
            compra = Compra.objects.all()
            for c in compra:
                data.append([
                    c.fecha_compra.strftime('%d-%m-%Y'),
                    str(c.proveedor),
                    format(c.subtotal, '.2f'),
                    format(c.iva, '.2f'),
                    format(c.total, '.2f'),
                    c.id,
                    c.get_estado_display()
                ])
        else:
            compra = Compra.objects.filter(fecha_compra__range=[start_date, end_date])
            for c in compra:
                data.append([
                    c.fecha_compra.strftime('%d-%m-%Y'),
                    str(c.proveedor),
                    format(c.subtotal, '.2f'),
                    format(c.iva, '.2f'),
                    format(c.total, '.2f'),
                    c.id,
                    c.get_estado_display()
                ])
    except:
        pass
    return JsonResponse(data, safe=False)


@csrf_exempt
def crear(request):
    data = {}
    if request.method == 'POST':
        datos = json.loads(request.POST['compras'])
        if datos:
            with transaction.atomic():
                c = Compra()
                c.fecha_compra = datos['fecha_compra']
                c.proveedor_id = datos['proveedor']
                c.user_id = request.user.id
                c.subtotal = float(datos['subtotal'])
                c.iva = float(datos['iva'])
                c.total = float(datos['total'])
                c.save()
                for i in datos['insumos']:
                    dv = Detalle_compra()
                    dv.compra_id = c.id
                    dv.insumo_id = i['id']
                    dv.cantidad = int(i['cantidad'])
                    dv.subtotal = float(i['subtotal'])
                    x = Insumo.objects.get(pk=i['id'])
                    dv.pvp_moment = float(x.pvp)
                    x.stock = x.stock + int(i['cantidad'])
                    dv.save()
                    x.save()
                    data['id'] = c.id
                    data['resp'] = True
        else:
            data['resp'] = False
            data['error'] = "Datos Incompletos"
    return HttpResponse(json.dumps(data), content_type="application/json")


def editar(request, id):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../../compra/get_insumo',
        'boton': 'Editar Compra', 'action': 'edit', 'titulo': 'Editar Registro de una Compra',
        'key': id
    }
    compra = Compra.objects.get(id=id)
    if request.method == 'GET':
        data['form'] = CompraForm(instance=compra)
        data['form2'] = Detalle_CompraForm()
        data['detalle'] = json.dumps(get_detalle_productos(id))
    return render(request, 'front-end/compra/compra_form.html', data)


@csrf_exempt
def editar_save(request):
    data = {}
    datos = json.loads(request.POST['compras'])
    if request.POST['action'] == 'edit':
        with transaction.atomic():
            c = Compra.objects.get(pk=request.POST['key'])
            c.fecha_compra = datos['fecha_compra']
            c.proveedor_id = datos['proveedor']
            c.subtotal = float(datos['subtotal'])
            c.iva = float(datos['iva'])
            c.total = float(datos['total'])
            c.save()
            c.detalle_compra_set.all().delete()
            for i in datos['insumos']:
                dv = Detalle_compra()
                dv.compra_id = c.id
                dv.insumo_id = i['id']
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
        for i in Detalle_compra.objects.filter(compra_id=id):
            iva_emp = Empresa.objects.get(pk=1)
            item = i.insumo.toJSON()
            item['cantidad'] = i.cantidad
            item['iva_emp'] = format(iva_emp.iva, '.2f')
            data.append(item)
    except:
        pass
    return data


@csrf_exempt
def get_insumo(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            insumo = Insumo.objects.filter(pk=id)
            iva_emp = Empresa.objects.get(pk=1)
            data = []
            for i in insumo:
                item = i.toJSON()
                item['cantidad'] = 1
                item['subtotal'] = 0.00
                item['iva_emp'] = iva_emp.iva
                data.append(item)
        else:
            data['error'] = 'No ha selecionado ningun Insumo'
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
            for p in Detalle_compra.objects.filter(compra_id=id):
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
            with transaction.atomic():
                es = Compra.objects.get(id=id)
                es.estado = 0
                for i in Detalle_compra.objects.filter(compra_id=id):
                    ch = Insumo.objects.get(pk=i.insumo.pk)
                    if ch.stock == 0:
                        data['error'] = 'No se puede devolver esta compra porque los insumos ya fueron utilizados'
                        data['content'] = 'Prueba con otra venta'
                    else:
                        if ch.stock < i.cantidad:
                            data['error'] = 'No se puede devolver esta compra porque los insumos ya fueron utilizados'
                            data['content'] = 'Prueba con otra venta'
                        else:
                            ch.stock = int(ch.stock) - int(i.cantidad)
                            es.save()
                            ch.save()
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
            es = Compra.objects.get(id=id)
            es.delete()
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)


@csrf_exempt
def index(request):
    data = {}
    try:
        action = request.POST['action']
        if action == 'table':
            data = [[i.fecha_compra.strftime("%d/%m/%Y"), i.proveedor.nombres, format(i.total, '.2f'),
                     i.get_estado_display()]
                    for i in Compra.objects.filter(estado=1, fecha_compra__month=datetime.now().month)]
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return HttpResponse(json.dumps(data), content_type="application/json")\


@csrf_exempt
def grap(request):
    data = {}
    try:
        action = request.POST['action']
        if action == 'chart':
            data = {
                'name': 'Porcentaje de compra',
                'colorByPoint': True,
                'data': grap_data(),
            }
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


def grap_data():
    year = datetime.now().year
    month = datetime.now().month
    data = []
    for i in Insumo.objects.all():
        total = Detalle_compra.objects.filter(insumo_id=i.id, compra__fecha_compra__year=year-1, compra__estado=1)\
            .aggregate(r=Coalesce(Sum('compra__total'), 0)).get('r')
        data.append({
            'name': i.nombre,
            'y': float(total)
        })
    return data


class printpdf(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('front-end/report/pdf_compra.html')
            context = {'title': 'Comprobante de Compra',
                       'sale': Compra.objects.get(pk=self.kwargs['pk']),
                       'empresa': Empresa.objects.get(id=1),
                       'icon': 'media/canteros_logo.png'
                       }
            html = template.render(context)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('compra:lista'))
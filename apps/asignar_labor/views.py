import json
from datetime import date, datetime
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.Mixins import SuperUserRequiredMixin
from apps.asignar_labor.forms import Asig_LaborForm, Asig_LaborForm_pag
from apps.asignar_labor.models import Asig_labor
from apps.historial_pagos.models import Pago
from apps.labor.models import Labor
from apps.trabajador.models import Trabajador
from apps.periodo.models import Periodo

opc_icono = 'fa fa-shopping-bag'
opc_entidad = 'Asignacion de Labores'
crud = '/asig_labor/crear'


class lista(SuperUserRequiredMixin, ListView):
    model = Asig_labor
    template_name = 'front-end/asig_labor/asig_labor_list.html'

    def get_queryset(self):
        queryset = Trabajador.objects.order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Asignacion de Labores'
        data['titulo'] = 'Listado de Asignacion de Labores'
        data['nuevo'] = '/asig_labor/nuevo'
        data['object_list'] = self.get_queryset()
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


def days_between(d1, d2):
    return abs(d2 - d1).days


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


@csrf_exempt
def get_detalle(request):
    data = {}
    try:
        id = request.POST['id']

        if id:
            data = []
            for p in Asig_labor.objects.filter(trabajador_id=id):
                items = p.toJSON()
                data.append(items)
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


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


@csrf_exempt
def save_asig(request):
    data = {}
    if request.method == 'POST':
        datos = json.loads(request.POST['asignaciones'])
        if datos:
            with transaction.atomic():
                for i in datos['trabajadores']:
                    d1 = datetime.strptime(i['desde'], '%Y-%m-%d')
                    d2 = datetime.strptime(i['hasta'], '%Y-%m-%d')
                    if Asig_labor.objects.filter(desde__lt=d2, hasta__gt=d1, trabajador_id=i['trabajador']):
                        t = Asig_labor.objects.get(trabajador_id=i['trabajador'])
                        data['resp'] = False
                        data['error'] = "El trabajador " + t.trabajador.nombres + " " + t.trabajador.apellidos + \
                                        " ya tiene Labores asignadas de " + t.desde.strftime('%d/%m/%Y') + " hasta " \
                                        + t.hasta.strftime('%d/%m/%Y') + ""
                    else:
                        dias = (days_between(d1, d2) + 1)
                        lab = Labor.objects.get(pk=i['labor'])
                        dv = Asig_labor()
                        dv.fecha_asig = datos['fecha_asig']
                        dv.periodo_id = datos['periodo']
                        dv.trabajador_id = i['trabajador']
                        dv.labor_id = i['labor']
                        dv.desde = i['desde']
                        dv.hasta = i['hasta']
                        dv.total_dias = dias
                        dv.valor_a_pag = dias * lab.valor_dia
                        dv.saldo = dias * lab.valor_dia
                        dv.save()
                        data['resp'] = True
        else:
            data['resp'] = False
            data['error'] = "Datos Incompletos"
    return HttpResponse(json.dumps(data), content_type="application/json")


def pago_jornada(request, id):
    jornada = Asig_labor.objects.get(id=id)
    opc_edit = '/asig_labor/save_pago'
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': opc_edit,
        'boton': 'Guardar Pago', 'titulo': 'Pago de jornada', 'id': id
    }
    if request.method == 'GET':
        form = Asig_LaborForm_pag(instance=jornada)
        data['form'] = form
    return render(request, 'front-end/asig_labor/asig_labor_form_pago.html', data)


@csrf_exempt
def save_pago(request):
    data = {}
    if request.method == 'POST':
        datos = json.loads(request.POST['valores'])
        if datos:
            with transaction.atomic():
                dv = Asig_labor.objects.get(pk=datos['id'])
                dv.valor_pag = float(dv.valor_pag) + float(datos['valor_pag'])
                dv.saldo = float(dv.saldo) - float(datos['valor_pag'])
                dv.save()
                hp = Pago()
                hp.fecha = datetime.now()
                hp.valor = float(datos['valor_pag'])
                hp.asignacion_id = dv.id
                hp.user_id = request.user.id
                hp.save()
                if dv.saldo == 0.0:
                    dv.estado = 1
                    dv.save()
                data['resp'] = True
        else:
            data['resp'] = False
            data['error'] = "Datos Incompletos"
    return HttpResponse(json.dumps(data), content_type="application/json")


def report(request):
    data = { 'icono': opc_icono, 'entidad': opc_entidad, 'titulo': 'Reporte de Asignacion de Labores', 'key': ''}
    return render(request, 'front-end/asig_labor/asig_labor_report.html', data)


@csrf_exempt
def data(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')

    try:
        if start_date == '' and end_date == '':
            print("sin fecha")
            asig_labor = Asig_labor.objects.all()
            for c in asig_labor:
                data.append([
                    c.fecha_asig.strftime('%d-%m-%Y'),
                    c.periodo.nombre,
                    c.trabajador.nombres + " " + c.trabajador.apellidos,
                    c.trabajador.get_estado_display(),
                    c.desde.strftime('%d-%m-%Y'),
                    c.hasta.strftime('%d-%m-%Y'),
                    c.labor.nombre,
                    c.total_dias,
                    format(c.valor_a_pag, '.2f'),
                    format(c.saldo, '.2f'),
                    format(c.valor_pag, '.2f'),
                    c.get_estado_display(),
                ])
        else:
            print("con fecha")
            asig_labor = Asig_labor.objects.filter(fecha_asig__range=[start_date, end_date])
            for c in asig_labor:
                data.append([
                    c.fecha_asig.strftime('%d-%m-%Y'),
                    c.periodo.nombre,
                    c.trabajador.nombres + " " + c.trabajador.apellidos,
                    c.trabajador.get_estado_display(),
                    c.desde.strftime('%d-%m-%Y'),
                    c.hasta.strftime('%d-%m-%Y'),
                    c.labor.nombre,
                    c.total_dias,
                    format(c.valor_a_pag, '.2f'),
                    format(c.saldo, '.2f'),
                    format(c.valor_pag, '.2f'),
                    c.get_estado_display()
                ])
    except:
        pass
    return JsonResponse(data, safe=False)

import json
from datetime import date, datetime
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.asignar_labor.forms import Asig_LaborForm, Asig_LaborForm_pag
from apps.asignar_labor.models import Asig_labor
from apps.historial_pagos.models import Pago
from apps.labor.models import Labor
from apps.trabajador.models import Trabajador
from apps.periodo.models import Periodo

opc_icono = 'fas fa-hand-holding-usd'
opc_entidad = 'Historial de pago de Labores'


def report(request):
    data = { 'icono': opc_icono, 'entidad': opc_entidad, 'titulo': 'Reporte de Historial de pago de Labores', 'key': ''}
    return render(request, 'front-end/historial_pagos/historial_pagos_report.html', data)


@csrf_exempt
def data(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')

    try:
        if start_date == '' and end_date == '':
            pago = Pago.objects.all()
            for c in pago:
                data.append([
                    c.fecha.strftime('%d-%m-%Y'),
                    c.asignacion.fecha_asig.strftime('%d-%m-%Y'),
                    c.asignacion.trabajador.nombres + " " + c.asignacion.trabajador.apellidos,
                    c.asignacion.trabajador.get_estado_display(),
                    c.asignacion.desde.strftime('%d-%m-%Y') + " / "+c.asignacion.hasta.strftime('%d-%m-%Y'),
                    c.asignacion.labor.nombre,
                    c.asignacion.total_dias,
                    format(c.asignacion.valor_a_pag, '.2f'),
                    format(c.asignacion.saldo, '.2f'),
                    format(c.valor, '.2f')
                ])
        else:
            pago = Pago.objects.filter(fecha__range=[start_date, end_date])
            for c in pago:
                data.append([
                    c.fecha.strftime('%d-%m-%Y'),
                    c.asignacion.fecha_asig,
                    c.asignacion.trabajador.nombres + "" + c.asignacion.trabajador.apellidos,
                    c.asignacion.trabajador.get_estado_display(),
                    c.asignacion.desde.strftime('%d-%m-%Y') + c.asignacion.hasta.strftime('%d-%m-%Y'),
                    c.asignacion.labor.nombre,
                    c.asignacion.total_dias,
                    format(c.asignacion.valor_a_pag, '.2f'),
                    format(c.asignacion.saldo, '.2f'),
                    format(c.valor, '.2f')
                ])
    except:
        pass
    return JsonResponse(data, safe=False)

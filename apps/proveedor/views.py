from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.http import HttpResponse, JsonResponse

from apps.cliente.models import Cliente
from apps.proveedor.forms import ProveedorForm
from apps.proveedor.models import Proveedor
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

from apps.trabajador.models import Trabajador

opc_icono = 'fa fa-truck'
opc_entidad = 'Proveedor'
crud = '/proveedor/crear'


def proveedor_lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nuevo Proveedor', 'titulo': 'Listado de Proveedor',
        'nuevo': '/proveedor/nuevo'
    }
    list = Proveedor.objects.all()
    data['list'] = list
    return render(request, "front-end/proveedor/proveedor_list.html", data)


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Proveedor', 'action': 'add', 'titulo': 'Nuevo Registro de un Proveedor',
    }
    if request.method == 'GET':
        data['form'] = ProveedorForm()
    return render(request, 'front-end/proveedor/proveedor_form.html', data)


def crear(request):
    f = ProveedorForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Proveedor', 'action': 'add', 'titulo': 'Nuevo Registro de un Proveedor'
    }
    action = request.POST['action']
    data['action'] = action
    data['form'] = ProveedorForm(request.POST)
    if request.method == 'POST' and 'action' in request.POST:
        f = ProveedorForm(request.POST)
        if f.is_valid():
            f.save(commit=False)
            if int(f.data['documento']) == 0:
                if Trabajador.objects.filter(cedula=f.data['numero_documento']):
                    data['error'] = 'Numero de Cedula ya exitente en los Trabajadores'
                    data['form'] = f
                else:
                    if Cliente.objects.filter(tipo_doc=1, numero_doc=f.data['numero_documento']):
                        data['error'] = 'Numero de Cedula ya exitente en los Proveedores'
                        data['form'] = f
                    else:
                        a = verificar(f.data['numero_documento'])
                        if a == False:
                            data['error'] = 'Numero de Cedula no coressponde a digitos para Ecuador'
                            data['form'] = f
                        else:
                            f.save()
                            return HttpResponseRedirect('/proveedor/lista')
            else:
                if Cliente.objects.filter(tipo_doc=0, numero_doc=f.data['numero_documento']):
                    data['error'] = 'Numero de Ruc ya exitente en los Clientes'
                    data['form'] = f
                else:
                    a = verificar(f.data['numero_documento'])
                    if a == False:
                        data['error'] = 'Numero de Ruc no coressponde a digitos para Ecuador'
                        data['form'] = f
                    else:
                        f.save()
                        return HttpResponseRedirect('/proveedor/lista')
        else:
            data['form'] = f
        return render(request, 'front-end/proveedor/proveedor_form.html', data)
    else:
        data['form'] = f
    return render(request, 'front-end/proveedor/proveedor_form.html', data)


def editar(request, id):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Guardar Edicion', 'action': 'add', 'titulo': 'Editar Registro de un Proveedor',
    }
    proveedor = Proveedor.objects.get(id=id)
    data['crud'] = '/proveedor/editar/' + str(id)
    data['option'] = 'editar'

    if request.method == 'GET':
        f = ProveedorForm(instance=proveedor)
        data['form'] = f
    else:
        f = ProveedorForm(request.POST, instance=proveedor)
        if f.is_valid():
            f.save(commit=False)
            if int(f.data['documento']) == 0:
                if Trabajador.objects.filter(cedula=f.data['numero_documento']):
                    data['error'] = 'Numero de Cedula ya exitente en los Trabajadores'
                    data['form'] = f
                else:
                    if Cliente.objects.filter(tipo_doc=1, numero_doc=f.data['numero_documento']):
                        data['error'] = 'Numero de Cedula ya exitente en los Proveedores'
                        data['form'] = f
                    else:
                        f.save()
                        return HttpResponseRedirect('/proveedor/lista')
            else:
                if Cliente.objects.filter(tipo_doc=1, numero_doc=f.data['numero_documento']):
                    data['error'] = 'Numero de Cedula ya exitente en los Clientes'
                    data['form'] = f
                else:
                    f.save()
                    return HttpResponseRedirect('/proveedor/lista')
        else:
            data['form'] = f
        return render(request, 'front-end/proveedor/proveedor_form.html', data)
    data['form'] = f
    return render(request, 'front-end/proveedor/proveedor_form.html', data)


def verificar(nro):
    error = ''
    l = len(nro)
    if l == 10 or l == 13:  # verificar la longitud correcta
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 22:  # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6:  # numeros enter 0 y 6
                if l == 10:
                    return __validar_ced_ruc(nro, 0)
                elif l == 13:
                    return __validar_ced_ruc(nro, 0) and nro[
                                                         10:13] != '000'  # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                return __validar_ced_ruc(nro, 1)  # sociedades publicas
            elif tercer_dig == 9:  # si es ruc
                return __validar_ced_ruc(nro, 2)  # sociedades privadas
            else:
                error = 'Tercer digito invalido'
                return False and error
        else:
            error = 'Codigo de provincia incorrecto'
            return False and error
    else:
        error = 'Longitud incorrecta del numero ingresado'
        return False and error


def __validar_ced_ruc(nro, tipo):
    total = 0
    if tipo == 0:  # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])  # digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1:  # r.u.c. publicos
        base = 11
        d_ver = int(nro[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2)
    elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(nro[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    for i in range(0, len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
        else:
            total += p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = Proveedor.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = "!No se puede eliminar este proveedor porque esta referenciado en otros procesos!!"
        data['content'] = "Intenta con otro proveedor"
    return JsonResponse(data)

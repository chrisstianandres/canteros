import json

from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.cliente.models import Cliente
from apps.proveedor.models import Proveedor
from apps.trabajador.forms import TrabajadorForm
from apps.trabajador.models import Trabajador

opc_icono = 'fas fa-people-carry'
opc_entidad = 'Trabajador'
crud = '/trabajador/crear'


def lista(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Nuevo Trabajador', 'titulo': 'Listado de Trabajador',
        'nuevo': '/trabajador/nuevo'
    }
    list = Trabajador.objects.all()
    data['list'] = list
    return render(request, "front-end/trabajador/trabajador_list.html", data)


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Trabajador', 'action': 'add', 'titulo': 'Nuevo Registro de un Trabajador',
    }
    if request.method == 'GET':
        data['form'] = TrabajadorForm()
    return render(request, 'front-end/trabajador/trabajador_form.html', data)


def crear(request):
    f = TrabajadorForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Trabajador', 'action': 'add', 'titulo': 'Nuevo Registro de un Trabajador'
    }
    action = request.POST['action']
    data['action'] = action
    data['form'] = TrabajadorForm(request.POST)
    if request.method == 'POST' and 'action' in request.POST:
        f = TrabajadorForm(request.POST)
        if f.is_valid():
            f.save(commit=False)
            if Cliente.objects.filter(tipo_doc=1, numero_doc=f.data['cedula']):
                data['error'] = 'Numero de Cedula ya exitente en los Clientes'
                data['form'] = f
            else:
                if Proveedor.objects.filter(documento=0, numero_documento=f.data['cedula']):
                    data['error'] = 'Numero de Cedula ya exitente en los Proveedores'
                    data['form'] = f
                else:
                    a = verificar(f.data['cedula'])
                    if a == False:
                        data['error'] = 'Numero de Cedula no coressponde a digitos para Ecuador'
                        data['form'] = f
                    else:
                        f.save()
                        return HttpResponseRedirect('/trabajador/lista')
        else:
            data['form'] = f
        return render(request, 'front-end/trabajador/trabajador_form.html', data)
    else:
        data['form'] = f
    return render(request, 'front-end/trabajador/trabajador_form.html', data)


def editar(request, id):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad,
        'boton': 'Guardar Edicion', 'action': 'add', 'titulo': 'Editar Registro de un Trabajador',
    }
    trabajador = Trabajador.objects.get(id=id)
    data['crud'] = '/trabajador/editar/' + str(id)
    data['option'] = 'editar'

    if request.method == 'GET':
        f = TrabajadorForm(instance=trabajador)
        data['form'] = f
    else:
        f = TrabajadorForm(request.POST, instance=trabajador)
        if f.is_valid():
            f.save(commit=False)

            if Cliente.objects.filter(tipo_doc=1, numero_doc=f.data['cedula']):
                data['error'] = 'Numero de Cedula ya exitente en los Trabajadores'
                data['form'] = f
            else:
                if Proveedor.objects.filter(documento=0, numero_documento=f.data['cedula']):
                    data['error'] = 'Numero de Cedula ya exitente en los Proveedores'
                    data['form'] = f
                else:
                    f.save()
                    return HttpResponseRedirect('/trabajador/lista')
        else:
            data['form'] = f
        return render(request, 'front-end/trabajador/trabajador_form.html', data)
    data['form'] = f
    return render(request, 'front-end/trabajador/trabajador_form.html', data)


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

import json

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from apps.Mixins import SuperUserRequiredMixin
from apps.cliente.models import Cliente
from apps.proveedor.models import Proveedor
from apps.user.forms import UserForm
from apps.user.models import User

opc_icono = 'fas fa-people-carry'
opc_entidad = 'Usuarios'
crud = '/user/crear'


class lista(SuperUserRequiredMixin, ListView):
    model = User
    template_name = 'front-end/user/user_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Usuario'
        data['titulo'] = 'Listado de Usuarios'
        data['nuevo'] = '/user/nuevo'
        return data


@csrf_exempt
def data(request):
    data = []
    try:
        user = User.objects.all()
        for c in user:
            print(c)
            data.append([
                c.id,
                c.username,
                c.get_full_name(),
                c.cedula,
                c.direccion,
                c.telefono,
                c.get_sexo_display(),
                c.id,
            ])
    except:
        pass
    return JsonResponse(data, safe=False)


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Usuario', 'action': 'add', 'titulo': 'Nuevo Registro de un Usuario',
        'option': 'add'
    }
    if request.method == 'GET':
        data['form'] = UserForm()
    return render(request, 'front-end/user/user_form.html', data)


def crear(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Usuario', 'action': 'add', 'titulo': 'Nuevo Registro de un Usuario', 'option': 'add'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = UserForm(request.POST, request.FILES)
            if f.is_valid():
                f.save(commit=False)
                if Proveedor.objects.filter(documento=0, numero_documento=f.data['cedula']):
                    data['error'] = 'Numero de Cedula ya exitente en los Proveedores'
                    data['form'] = f
                elif Cliente.objects.filter(tipo_doc=1, numero_doc=f.data['cedula']):
                    data['error'] = 'Numero de Cedula ya exitente en los Clientes'
                    data['form'] = f
                elif verificar(f.data['cedula']):
                    f.save()
                    nw = f.save()
                    return HttpResponseRedirect('/user/lista')
                else:
                    data['error'] = 'Numero de Cedula no valido para Ecuador'
                    data['form'] = f
            else:

                data['form'] = f
            return render(request, 'front-end/user/user_form.html', data)


def editar(request, id):
    user = User.objects.get(id=id)
    crud = '/user/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un User',
        'option': 'editar'
    }
    if request.method == 'GET':
        form = UserForm(instance=user)
        data['form'] = form
    else:
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            nw = form.save()
            return HttpResponseRedirect('/user/lista')
        else:
            data['form'] = form
    return render(request, 'front-end/user/user_form.html', data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = User.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = 'No se puede eliminar este Usuario porque esta referenciado en otros procesos'
        data['content'] = 'Intenta con otro Usuario'
    return JsonResponse(data)


def verificar(nro):
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
def estado(request):
    data = {}
    try:
        id = int(request.POST['id'])
        ps = User.objects.get(pk=id)
        if ps.estado == 1:
            ps.estado = 0
            ps.save()
            data['resp'] = True
        elif ps.estado == 0:
            ps.estado = 1
            ps.save()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)


def profile(request):
    user = User.objects.get(id=request.user.id)
    crud = '/user/profile'
    data = {
        'icono': 'fa fa-user', 'entidad': 'Perfil de Usuario', 'crud': crud,
        'boton': 'Guardar info', 'action': 'add', 'titulo': 'Perfil de Usuario'
    }
    if request.method == 'GET':
        form = UserForm(instance=user)
        data['form'] = form
    else:
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return HttpResponseRedirect('/user/profile')
    return render(request, 'front-end/profile/profile.html', data)
    # return render(request, 'front-end/profile.html', data)

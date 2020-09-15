"""canteros URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.urls import path
from apps import backEnd as backEnd
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # empresa
    path('empresa/', include('apps.configuracion.urls', namespace='empresa')),
    path('', login_required(backEnd.menu), name='menu'),
    path('login/', backEnd.logeo, name='login'),
    path('logout/', backEnd.disconnect, name='logout'),
    path('connect/', backEnd.connect, name='connect'),
    path('user/', include('apps.user.urls', namespace='user')),
    path('cliente/', include('apps.cliente.urls', namespace='cliente')),
    path('proveedor/', include('apps.proveedor.urls', namespace='proveedor')),
    path('insumo/', include('apps.insumo.urls', namespace='insumo')),
    path('trabajador/', include('apps.trabajador.urls', namespace='trabajador')),
    path('cantero/', include('apps.cantero.urls', namespace='cantero')),
    path('producto/', include('apps.producto.urls', namespace='producto')),
    path('categoria/', include('apps.categoria.urls', namespace='categoria')),
    path('presentacion/', include('apps.presentacion.urls', namespace='presentacion')),
    path('compra/', include('apps.compra.urls', namespace='compra')),
    path('venta/', include('apps.venta.urls', namespace='venta')),
    path('periodo/', include('apps.periodo.urls', namespace='periodo')),
    path('asig_insumo/', include('apps.asignar_insumo.urls', namespace='asig_insumo')),
    path('asig_labor/', include('apps.asignar_labor.urls', namespace='asig_labor')),
    path('pagos/', include('apps.historial_pagos.urls', namespace='pagos')),
    path('labor/', include('apps.labor.urls', namespace='labor')),
    path('produccion/', include('apps.produccion.urls', namespace='produccion')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



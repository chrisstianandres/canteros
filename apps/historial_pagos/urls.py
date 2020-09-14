from django.conf.urls import url
from django.urls import path
from . import views
from apps.historial_pagos.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Historial_pagos'

urlpatterns = [
    path('report', login_required(views.report), name='report'),
    path('data', login_required(views.data), name='data'),
]

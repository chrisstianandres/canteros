from django.conf.urls import url
from django.urls import path
from . import views
from apps.cantero.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Cantero'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('nuevo', login_required(views.nuevo), name='nuevo'),
    path('crear', login_required(views.crear), name='crear'),
    #path('editar/<int:id_alumno>', login_required(views.editar), name='editar'),

]

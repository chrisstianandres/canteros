from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'Insumos'

urlpatterns = [
    path('lista', login_required(views.lista), name='lista'),
    path('nuevo', login_required(views.nuevo), name='nuevo'),
    path('crear', login_required(views.crear), name='crear'),
    path('ajax', login_required(views.ajax), name='ajax'),
    path('editar/<int:id>', login_required(views.editar), name='editar'),
    path('eliminar', login_required(views.eliminar), name='eliminar'),

]

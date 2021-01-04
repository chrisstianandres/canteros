from django.contrib import admin
from .models import *


class Asig_Admin(admin.TabularInline):
    model = Detalle_asig_insumo


class Detalle_asigAdmin(admin.ModelAdmin):
    inlines = (Asig_Admin,)


admin.site.register(Asig_insumo, Detalle_asigAdmin)

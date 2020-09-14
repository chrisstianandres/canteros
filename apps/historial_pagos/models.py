from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import model_to_dict

from apps.asignar_labor.models import Asig_labor


class Pago(models.Model):
    fecha = models.DateField(default=datetime.now)
    asignacion = models.ForeignKey(Asig_labor, on_delete=models.PROTECT)
    valor = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return '%s %s' % (self.fecha, self.asignacion.trabajador.nombres)

    def toJSON(self):
        item = model_to_dict(self)
        item['asignacion'] = self.asignacion.toJSON()
        return item

    class Meta:
        db_table = 'historial_pago'
        verbose_name = 'historial_pago'
        verbose_name_plural = 'historial_pagos'

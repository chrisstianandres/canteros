from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.labor.models import Labor
from apps.periodo.models import Periodo
from apps.trabajador.models import Trabajador


class Asig_labor(models.Model):
    fecha_asig = models.DateField(default=datetime.now)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT)
    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT)
    labor = models.ForeignKey(Labor, on_delete=models.CASCADE)
    desde = models.DateField(default=datetime.now)
    hasta = models.DateField(default=datetime.now)

    def __str__(self):
        return '%s %s' % (self.fecha_asig, self.trabajador.nombres)

    def toJSON(self):
        item = model_to_dict(self)
        item['trabajador'] = self.trabajador.toJSON()
        item['labor'] = self.labor.toJSON()
        item['periodo'] = self.periodo.toJSON()
        return item

    class Meta:
        db_table = 'asig_labor'
        verbose_name = 'asig_labor'
        verbose_name_plural = 'asig_labor'
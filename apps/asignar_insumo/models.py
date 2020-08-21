from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.insumo.models import Insumo
from apps.cantero.models import Cantero
from apps.periodo.models import Periodo


class Asig_insumo(models.Model):
    fecha_asig = models.DateField(default=datetime.now)
    cantero = models.ForeignKey(Cantero, on_delete=models.PROTECT)
    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT)

    def __str__(self):
        return '%s %s' % (self.fecha_asig, self.cantero.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['cantero'] = self.cantero.toJSON()
        item['periodo'] = self.periodo.toJSON()
        return item

    class Meta:
        db_table = 'asig_insumo'
        verbose_name = 'asig_insumo'
        verbose_name_plural = 'asig_insumo'


class Detalle_asig_insumo(models.Model):
    asig_insumo = models.ForeignKey(Asig_insumo, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return '%s %s' % (self.asig_insumo, self.insumo.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['compra'] = self.asig_insumo.toJSON()
        item['insumo'] = self.insumo.toJSON()
        return item

    class Meta:
        db_table = 'detalle_asig_insumo'
        verbose_name = 'detalle_asig_insumo'
        verbose_name_plural = 'detalles_asig_insumos'
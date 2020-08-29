from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.cantero.models import Cantero
from apps.labor.models import Labor
from apps.periodo.models import Periodo
from apps.presentacion.models import Presentacion
from apps.producto.models import Producto
from apps.trabajador.models import Trabajador


class Produccion(models.Model):
    fecha = models.DateField(default=datetime.now)
    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT)
    cantero = models.ForeignKey(Cantero, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.fecha, self.cantero.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['cantero'] = self.cantero.toJSON()
        item['periodo'] = self.periodo.toJSON()
        item['producto'] = self.producto.toJSON()
        return item

    class Meta:
        db_table = 'produccion'
        verbose_name = 'produccion'
        verbose_name_plural = 'producciones'
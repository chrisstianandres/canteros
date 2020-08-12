from datetime import datetime
from django.db import models
from apps.insumo.models import Insumo
from apps.presentacion.models import Presentacion
from apps.proveedor.models import Proveedor

area = (
    (1, 'METROS'),
    (0, 'HECTAREAS'),
)
estado = (
    (0, 'ACTIVO'),
    (1, 'INACTIVO')
)


class Compra(models.Model):
    fecha_compra = models.DateField(default=datetime.now)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.IntegerField(choices=estado, default=1)

    def __str__(self):
        return '%s %s' % (self.fecha_compra, self.proveedor.nombres)

    class Meta:
        db_table = 'compra'
        verbose_name = 'compra'
        verbose_name_plural = 'compras'
        ordering = ['id', 'proveedor']


from datetime import datetime
from django.db import models
from apps.cliente.models import Cliente

tipo = (
    (1, 'CEDULA'),
    (0, 'RUC'),
)


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_venta = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(max_digits=1000, decimal_places=2)
    iva = models.DecimalField(max_digits=1000, decimal_places=2)
    total = models.DecimalField(max_digits=1000, decimal_places=2)

    def __str__(self):
        return '%s %s %s' % (self.cliente, self.fecha_venta, self.total)

    class Meta:
        db_table = 'venta'
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
        ordering = ['id', 'cliente']
#
# class Detalle_venta(models.Model):
#     venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
#     producto
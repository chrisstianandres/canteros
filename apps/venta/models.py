from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from apps.cliente.models import Cliente
from apps.producto.models import Producto
from apps.user.models import User

estado = (
    (0, 'DEVUELTA'),
    (1, 'FINALIZADA')
)


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha_venta = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    estado = models.IntegerField(choices=estado, default=1)

    def __str__(self):
        return '%s %s %s' % (self.cliente, self.fecha_venta, self.total)

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        db_table = 'venta'
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
#


class Detalle_venta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    pvp_moment = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=1)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s %s' % (self.venta, self.producto.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['venta'] = self.venta.toJSON()
        item['producto'] = self.producto.toJSON()
        return item

    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'detalle_venta'
        verbose_name_plural = 'detalles_ventas'
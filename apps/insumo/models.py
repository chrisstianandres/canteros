from django.db import models
from django.forms import model_to_dict

from apps.categoria.models import Categoria
from apps.presentacion.models import Presentacion


class Insumo(models.Model):
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT, null=True, blank=True)
    descripcion = models.CharField(max_length=50)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):

        return '%s %s %s' % (self.nombre, '/', self.presentacion.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['presentacion'] = self.presentacion.toJSON()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    class Meta:
        db_table = 'insumo'
        verbose_name = 'insumo'
        verbose_name_plural = 'insumos'
        ordering = ['id', 'nombre']


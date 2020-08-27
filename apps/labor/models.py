from django.db import models
from django.forms import model_to_dict


class Labor(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    valor_dia = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):

        return '%s %s %s %s' % (self.nombre, '/', '$', self.valor_dia)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'labor'
        verbose_name = 'labor'
        verbose_name_plural = 'labores'
        ordering = ['id', 'nombre']


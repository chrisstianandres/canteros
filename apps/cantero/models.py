from django.db import models
from django.forms import model_to_dict

area = (
    (1, 'METROS'),
    (0, 'HECTAREAS'),
)
estado = (
    (0, 'ACTIVO'),
    (1, 'INACTIVO')
)


class Cantero(models.Model):
    nombre = models.CharField(max_length=50)
    dimesion = models.IntegerField(choices=area, default=1)
    valor_dim = models.FloatField(max_length=13)
    estado = models.IntegerField(choices=estado, default=1)

    def _area_total(self):
        if self.dimesion == 1:
            Area = self.valor_dim
            return Area
        else:
            Area = (self.valor_dim*1000)
            return Area
    area_total = property(_area_total)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return '%s %s' % (self.nombre, self.valor_dim)

    class Meta:
        db_table = 'cantero'
        verbose_name = 'cantero'
        verbose_name_plural = 'canteros'
        ordering = ['-nombre', '-valor_dim']


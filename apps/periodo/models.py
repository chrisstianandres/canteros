from django.db import models
from django.forms import model_to_dict

estado = (
    (1, 'ACTIVO'),
    (0, 'INACTIVO'),
)

class Periodo(models.Model):
    nombre = models.CharField(max_length=50)
    desde = models.DateField()
    hasta = models.DateField()
    estado = models.IntegerField(choices=estado, unique=True, default=0)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'periodo'
        verbose_name = 'periodo'
        verbose_name_plural = 'periodos'


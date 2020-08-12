from datetime import datetime
from django.db import models

tipo = (
    (1, 'CEDULA'),
    (0, 'RUC'),
)

class Empresa(models.Model):
    nombre = models.CharField(max_length=30)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.CharField(max_length=50)
    correo = models.CharField(max_length=50, null=True, blank=True, unique=True)
    telefono = models.CharField(max_length=10, unique=True)
    iva = models.DecimalField(max_digits=2, decimal_places=2, default=0.12)

    def __str__(self):
        return '%s %s' % (self.nombre, self.direccion)

    class Meta:
        db_table = 'empresa'
        verbose_name = 'empresa'



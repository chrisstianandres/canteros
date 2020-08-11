from django.db import models

tipo = (
    (1, 'CEDULA'),
    (0, 'RUC'),
)

class Insumo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % (self.nombre)

    class Meta:
        db_table = 'insumo'
        verbose_name = 'insumo'
        verbose_name_plural = 'insumos'
        ordering = ['-id', '-nombre']


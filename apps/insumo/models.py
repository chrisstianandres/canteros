from django.db import models


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


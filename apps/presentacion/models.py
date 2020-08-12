from django.db import models


class Presentacion(models.Model):
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.nombre, self.abreviatura

    class Meta:
        db_table = 'presnetacion'
        verbose_name = 'presentacion'
        verbose_name_plural = 'presentaciones'
        ordering = ['id', 'nombre']


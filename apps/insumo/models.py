from django.db import models

from apps.categoria.models import Categoria


class Insumo(models.Model):
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.nombre, self.categoria

    class Meta:
        db_table = 'insumo'
        verbose_name = 'insumo'
        verbose_name_plural = 'insumos'
        ordering = ['id', 'nombre']


from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.nombre

    class Meta:
        db_table = 'categoria'
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ['id', 'nombre']


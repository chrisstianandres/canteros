from django.db import models

genero = (
    (1, 'MASCULINO'),
    (0, 'FEMENINO'),
)


class Trabajador(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.IntegerField(choices=genero, default=1)
    cedula = models.CharField(max_length=10, unique=True)
    correo = models.CharField(max_length=50, null=True, blank=True, unique=True)
    telefono = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.nombres, self.direccion)

    class Meta:
        db_table = 'trabajador'
        verbose_name = 'trabajador'
        verbose_name_plural = 'trabajadores'
        ordering = ['-nombres', '-cedula']


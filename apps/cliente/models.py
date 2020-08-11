from django.db import models

tipo = (
    (1, 'CEDULA'),
    (0, 'RUC'),
)

class Cliente(models.Model):
    nombres = models.CharField(max_length=50)
    tipo_doc = models.IntegerField(choices=tipo, default=1)
    numero_doc = models.CharField(max_length=13, unique=True)
    correo = models.CharField(max_length=50, null=True, blank=True, unique=True)
    telefono = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.nombres, self.direccion)

    class Meta:
        db_table = 'cliente'
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        ordering = ['-nombres', '-numero_doc']


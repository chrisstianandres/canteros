# Generated by Django 2.2.15 on 2020-08-15 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0002_auto_20200813_0024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_compra',
            name='presentacion',
        ),
    ]

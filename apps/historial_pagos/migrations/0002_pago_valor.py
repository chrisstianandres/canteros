# Generated by Django 2.2.15 on 2020-09-14 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historial_pagos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
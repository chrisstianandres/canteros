# Generated by Django 2.2.15 on 2020-08-14 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('presentacion', '0001_initial'),
        ('insumo', '0002_auto_20200812_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='insumo',
            name='presentacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='presentacion.Presentacion'),
        ),
        migrations.AddField(
            model_name='insumo',
            name='pvp',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True),
        ),
    ]

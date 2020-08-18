# Generated by Django 2.2.15 on 2020-08-15 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0003_remove_detalle_compra_presentacion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compra',
            options={'ordering': ['-id', 'proveedor'], 'verbose_name': 'compra', 'verbose_name_plural': 'compras'},
        ),
        migrations.AlterField(
            model_name='detalle_compra',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]

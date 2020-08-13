# Generated by Django 2.2.15 on 2020-08-12 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10)),
                ('ruc', models.CharField(max_length=13, unique=True)),
                ('direccion', models.CharField(max_length=50)),
                ('correo', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('telefono', models.CharField(max_length=10, unique=True)),
                ('iva', models.DecimalField(decimal_places=2, default=0.12, max_digits=2)),
            ],
            options={
                'verbose_name': 'empresa',
                'db_table': 'empresa',
            },
        ),
    ]
# Generated by Django 2.2.15 on 2020-08-29 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['id', 'nombre'],
                'verbose_name_plural': 'categorias',
                'db_table': 'categoria',
                'verbose_name': 'categoria',
            },
        ),
    ]

# Generated by Django 2.2.15 on 2020-08-10 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'insumo',
                'verbose_name_plural': 'insumos',
                'db_table': 'insumo',
                'ordering': ['-id', '-nombre'],
            },
        ),
    ]

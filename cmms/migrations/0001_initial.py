# Generated by Django 5.0.4 on 2024-04-23 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(db_index=True, unique=True, verbose_name='maquina')),
                ('codigo', models.CharField(max_length=25, verbose_name='codigoMaquina')),
            ],
            options={
                'verbose_name': 'maquina',
                'verbose_name_plural': 'maquinas',
                'db_table': 'maquinas',
                'ordering': ('codigo',),
            },
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(verbose_name='nombre')),
                ('codUser', models.IntegerField(unique=True, verbose_name='userCode')),
                ('puesto', models.CharField(choices=[('practicante', 'Practicante'), ('ingeniero', 'Ingeniero'), ('gerente', 'Gerente')], default='ingeniero', verbose_name='puesto')),
            ],
        ),
    ]

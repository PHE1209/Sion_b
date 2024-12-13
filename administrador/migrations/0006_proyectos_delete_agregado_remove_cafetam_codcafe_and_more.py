# Generated by Django 5.1.4 on 2024-12-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0005_rename_empresa_usuarios_empresa_alter_usuarios_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='proyectos',
            fields=[
                ('id_proyecto', models.AutoField(primary_key=True, serialize=False)),
                ('pm', models.CharField(max_length=25)),
                ('empresa', models.CharField(max_length=25)),
                ('nombre', models.CharField(max_length=25)),
                ('alcance', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'proyectos',
            },
        ),
        migrations.DeleteModel(
            name='Agregado',
        ),
        migrations.RemoveField(
            model_name='cafetam',
            name='codCafe',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='cargo',
        ),
        migrations.DeleteModel(
            name='Catalogos',
        ),
        migrations.RemoveField(
            model_name='comuna',
            name='id_provincia',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='id_comuna',
        ),
        migrations.RemoveField(
            model_name='sucursal',
            name='id_comuna',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='rut_persona',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='sucursal',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='codFormaPago',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='rut',
        ),
        migrations.DeleteModel(
            name='Postres',
        ),
        migrations.RemoveField(
            model_name='provincia',
            name='id_region',
        ),
        migrations.DeleteModel(
            name='Registro',
        ),
        migrations.DeleteModel(
            name='Tamanio',
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='telefono',
            field=models.CharField(max_length=15),
        ),
        migrations.DeleteModel(
            name='Cafe',
        ),
        migrations.DeleteModel(
            name='CafeTam',
        ),
        migrations.DeleteModel(
            name='Cargo',
        ),
        migrations.DeleteModel(
            name='Comuna',
        ),
        migrations.DeleteModel(
            name='Empleado',
        ),
        migrations.DeleteModel(
            name='Sucursal',
        ),
        migrations.DeleteModel(
            name='FormaPago',
        ),
        migrations.DeleteModel(
            name='Pedido',
        ),
        migrations.DeleteModel(
            name='Persona',
        ),
        migrations.DeleteModel(
            name='Provincia',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
    ]

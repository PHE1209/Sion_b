# Generated by Django 5.1.4 on 2025-01-25 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0007_alter_historicalprospecciones_coordenada_este_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humedad',
            name='id_proyecto',
            field=models.CharField(max_length=50),
        ),
    ]

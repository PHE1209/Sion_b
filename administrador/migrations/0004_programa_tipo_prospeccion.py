# Generated by Django 5.1.4 on 2025-01-20 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0003_programa'),
    ]

    operations = [
        migrations.AddField(
            model_name='programa',
            name='tipo_prospeccion',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]

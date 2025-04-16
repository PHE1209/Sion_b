# Generated by Django 5.0.13 on 2025-04-16 04:28

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0007_remove_historicalmuestreo_id_embalaje_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='densidad_insitu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_prospeccion', models.CharField(blank=True, max_length=25, null=True)),
                ('id_muestra', models.CharField(max_length=50)),
                ('profundidad_desde', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('profundidad_hasta', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('profundidad_promedio', models.DecimalField(decimal_places=3, max_digits=12)),
                ('profundidad_ensayo', models.DecimalField(decimal_places=3, max_digits=12)),
                ('horizonte', models.CharField(blank=True, max_length=50, null=True)),
                ('cota', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('profundidad_nivel_freatico', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('condicion_ambiental', models.CharField(blank=True, max_length=50, null=True)),
                ('peso_materia_humedo', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('masa_arena_inicial_en_cono_superior', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('masa_arena_remanente_en_cono_superior', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('masa_arena_en_cono_inferior', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('masa_arena_excavacion', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('densidad_aparente_arena', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('volumen_perforacion', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('densidad_natural_del_suelo', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('peso_suelo_humedo', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('peso_suelo_seco', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('peso_agua', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('humedad', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('densidad_seca_del_suelo', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('area', models.CharField(blank=True, max_length=50, null=True)),
                ('observacion', models.CharField(max_length=255)),
                ('id_prospeccion', models.ForeignKey(db_column='id_prospeccion', on_delete=django.db.models.deletion.CASCADE, to='administrador.prospecciones', to_field='id_prospeccion')),
                ('id_proyecto', models.ForeignKey(db_column='id_proyecto', on_delete=django.db.models.deletion.CASCADE, to='administrador.proyectos')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'densidad_insitu',
            },
        ),
        migrations.CreateModel(
            name='Historicaldensidad_insitu',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('tipo_prospeccion', models.CharField(blank=True, max_length=25, null=True)),
                ('id_muestra', models.CharField(max_length=50)),
                ('profundidad_desde', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('profundidad_hasta', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('profundidad_promedio', models.DecimalField(decimal_places=3, max_digits=12)),
                ('profundidad_ensayo', models.DecimalField(decimal_places=3, max_digits=12)),
                ('horizonte', models.CharField(blank=True, max_length=50, null=True)),
                ('cota', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('profundidad_nivel_freatico', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('condicion_ambiental', models.CharField(blank=True, max_length=50, null=True)),
                ('peso_materia_humedo', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('masa_arena_inicial_en_cono_superior', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('masa_arena_remanente_en_cono_superior', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('masa_arena_en_cono_inferior', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('masa_arena_excavacion', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('densidad_aparente_arena', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('volumen_perforacion', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('densidad_natural_del_suelo', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('peso_suelo_humedo', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('peso_suelo_seco', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('peso_agua', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('humedad', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('densidad_seca_del_suelo', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('area', models.CharField(blank=True, max_length=50, null=True)),
                ('observacion', models.CharField(max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('id_prospeccion', models.ForeignKey(blank=True, db_column='id_prospeccion', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='administrador.prospecciones', to_field='id_prospeccion')),
                ('id_proyecto', models.ForeignKey(blank=True, db_column='id_proyecto', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='administrador.proyectos')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical densidad_insitu',
                'verbose_name_plural': 'historical densidad_insitus',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

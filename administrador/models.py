from mailbox import NoSuchMailboxError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from datetime import timedelta, date, time
from decimal import Decimal
import json
import logging
from datetime import timedelta, date
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
import logging
from decimal import Decimal
from django.db import models
import logging
from decimal import Decimal
from django.db import models
import logging
from django.db import models
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User

# Tablas de ejemplo (sin cambios)
logger = logging.getLogger(__name__)
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)



# Proyectos ########################
logger = logging.getLogger(__name__)
class Proyectos(models.Model):
    id = models.CharField(max_length=25, primary_key=True)  # Sin restricción de formato
    estatus_proyecto = models.CharField(max_length=25, choices=[
        ('propuesta', 'Propuesta'),
        ('ejecucion', 'Ejecución'),
        ('standby', 'StandBy'),
    ], null=True)
    pm = models.CharField(max_length=50, null=False)
    empresa = models.CharField(max_length=50, null=False)
    nombre = models.CharField(max_length=255, null=False)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    alcance = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'proyectos'

    def __str__(self):
        return self.id



# ProyectoUsuario ########################
logger = logging.getLogger(__name__)
class ProyectoUsuario(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=25, choices=[
        ('admin', 'Administrador'),
        ('editor', 'Editor'),
        ('lector', 'Lector'),
    ], default='lector')
    asignado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'proyecto_usuario'
        unique_together = ('proyecto', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} - {self.proyecto.id} ({self.rol})"


# Prospecciones ########################
logger = logging.getLogger(__name__)
import logging
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.utils import timezone

logger = logging.getLogger(__name__)

class Prospecciones(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, choices=[
        ('sondajes', 'Sondajes'),
        ('calicatas', 'Calicatas'),
        ('geofisica', 'Geofísica'),
    ], null=False)
    tipo_sondaje = models.CharField(max_length=25, choices=[
        ('geotecnico', 'Geotécnico'),
        ('hidrogeologico', 'Hidrogeológico'),
        ('estratigrafico', 'Estratigráfico'),
        ('ambiental', 'Ambiental'),
        ('cimentacion', 'Cimentación'),
        ('petrolero', 'Petrolero'),
        ('minero', 'Minero'),
        ('sismico', 'Sísmico'),
        ('otro', 'Otro'),
    ], null=True, blank=True)
    metodologia_sondaje = models.CharField(max_length=25, choices=[
        ('diamantina', 'Diamantina'),
        ('rotopercusion', 'Rotopercusión'),
        ('helicoidal', 'Helicoidal'),
        ('circulacion_reversa', 'Circulación Reversa'),
        ('percusion_simple', 'Percusión Simple'),
        ('sonico', 'Sónico'),
        ('cpt_scptu', 'CPT/SCPTu'),
        ('geofisico', 'Geofísico'),
        ('direct_push', 'Direct Push'),
        ('reflexion_sismica', 'Reflexión Sísmica'),
        ('bombas_prueba', 'Bombas de Prueba'),
        ('pruebas_pilotes', 'Pruebas de Pilotes'),
        ('otro', 'Otro'),
    ], null=True, blank=True)
    metodologia_geofisica = models.CharField(max_length=25, choices=[
        ('reflexion_sismica', 'Reflexión Sísmica'),
        ('refraccion_sismica', 'Refracción Sísmica'),
        ('difraccion_sismica', 'Difracción Sísmica'),
        ('masw', 'MASW (Análisis Multicanal de Ondas Superficiales)'),
        ('downhole_crosshole', 'Sismología de perforación (Downhole & Crosshole)'),
        ('geotomografia_sismica', 'Geotomografía Sísmica'),
        ('resistividad_electrica', 'Resistividad Eléctrica'),
        ('polarizacion_inducida', 'Polarización Inducida'),
        ('sev', 'Sondeo Eléctrico Vertical (SEV)'),
        ('ert', 'Tomografía Eléctrica (ERT)'),
        ('tdem', 'Electromagnetismo de dominio de tiempo (TDEM)'),
        ('magnetotelurica', 'Magnetotelúrica (MT)'),
        ('magnetometria', 'Magnetometría'),
        ('gravimetria', 'Gravimetría'),
        ('microgravimetria', 'Microgravimetría'),
        ('georradar', 'Georradar (GPR)'),
        ('otro', 'Otro'),
    ], null=True, blank=True)
    id_prospeccion = models.CharField(max_length=25, null=False, unique=True)
    area = models.CharField(max_length=50, null=True, blank=True, default='Sin área definida')
    fecha_inicio_perforacion = models.DateField(null=True, blank=True)
    fecha_termino_perforacion = models.DateField(null=True, blank=True)
    coordenada_este = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
    coordenada_norte = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
    elevacion = models.IntegerField(null=True, blank=True)
    profundidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    inclinacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    diametro_sondaje = models.CharField(max_length=25, choices=[
        ('(AQ) 27 mm / 48 mm', '(AQ) 27 mm / 48 mm'),
        ('(BQ) 36 mm / 60 mm', '(BQ) 36 mm / 60 mm'),
        ('(NQ) 47 mm / 75 mm', '(NQ) 47 mm / 75 mm'),
        ('(HQ) 63 mm / 96 mm', '(HQ) 63 mm / 96 mm'),
        ('(PQ3) 83 mm / 122 mm', '(PQ3) 83 mm / 122 mm'),
        ('(PQ) 85 mm / 122 mm', '(PQ) 85 mm / 122 mm'),
        ('51 mm', '51 mm'),
        ('76 mm', '76 mm'),
        ('100 mm', '100 mm'),
        ('102 mm', '102 mm'),
        ('114 mm', '114 mm'),
        ('127 mm', '127 mm'),
        ('152 mm', '152 mm'),
        ('200 mm', '200 mm'),
        ('203 mm', '203 mm'),
        ('216 mm', '216 mm'),
        ('305 mm', '305 mm'),
        ('311 mm', '311 mm'),
        ('445 mm', '445 mm'),
        ('600 mm', '600 mm'),
        ('otro', 'Otro'),
    ], null=True, blank=True)
    habilitacion = models.CharField(max_length=25, choices=[
        ('si', 'Sí'),
        ('no', 'No'),
        ('na', 'Na'),
    ], null=True, blank=True)
    monolito = models.CharField(max_length=25, choices=[
        ('si', 'Sí'),
        ('no', 'No'),
        ('na', 'Na'),
    ], null=True, blank=True)
    tapado = models.CharField(max_length=25, choices=[
        ('si', 'Sí'),
        ('no', 'No'),
        ('na', 'Na'),
    ], null=True, blank=True)
    contratista = models.CharField(max_length=100, null=True, blank=True)
    marca_maquina1 = models.CharField(max_length=50, null=True, blank=True)
    modelo_maquina1 = models.CharField(max_length=50, null=True, blank=True)
    ppu1 = models.CharField(max_length=10, null=True, blank=True)
    marca_maquina2 = models.CharField(max_length=50, null=True, blank=True)
    modelo_maquina2 = models.CharField(max_length=50, null=True, blank=True)
    ppu2 = models.CharField(max_length=10, null=True, blank=True)
    observacion = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    imagenes = models.ManyToManyField('ProspeccionImage', related_name='prospeccion_imagenes')
    history = HistoricalRecords()

    class Meta:
        db_table = 'prospecciones'

    def __str__(self):
        return self.id_prospeccion

class ProspeccionImage(models.Model):
    prospeccion = models.ForeignKey('Prospecciones', on_delete=models.CASCADE, related_name='imagenes_asociadas')
    image = models.ImageField(upload_to='prospecciones/')
    
    class Meta:
        db_table = 'prospeccion_images'

    def __str__(self):
        return f"Imagen para Prospección {self.prospeccion.id_prospeccion}"

class Historial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'historial'

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha}"


# 1. Sondaje Geotécnico:
# Penetrómetro de Cono (CPT y SCPTu): Inserción de un cono en el suelo para medir resistencia y propiedades dinámicas.
# Sondaje Sónico: Utiliza vibraciones de alta frecuencia para perforar y obtener muestras inalteradas.
# Pruebas con helicoidal (Auger): Método superficial para evaluar estabilidad en terrenos blandos.
# 2. Sondaje Hidrogeológico:
# Rotopercusión: Combina rotación y golpes para perforar acuíferos.
# Circulación Inversa: Ideal para estudiar acuíferos profundos, utilizando aire o agua para extraer el material perforado.
# Bombas de Prueba: Evalúan caudal y calidad del agua subterránea.
# 3. Sondaje Estratigráfico:
# Diamantina: Extrae núcleos continuos del terreno para analizar capas geológicas.
# Sondaje Rotativo: Útil para estudiar la secuencia y composición de estratos a mediana profundidad.
# 4. Sondaje Ambiental:
# Sondaje Direct Push: Inserción directa para recolectar muestras rápidas de suelo o agua contaminada.
# Sondaje Eléctrico: Utiliza mediciones de resistividad para identificar contaminantes sin perforar extensivamente.
# 5. Sondaje de Cimentación:
# Penetrómetro Estático: Verifica la capacidad portante del suelo para estructuras.
# Método de Pruebas de Pilotes: Evalúa la resistencia y estabilidad de pilotes ya instalados.
# 6. Sondaje Petrolero:
# Perforación Rotatoria: Técnica estándar para explorar y extraer hidrocarburos.
# Registro de Pozos (Wireline Logging): Mide propiedades físicas y geológicas del pozo perforado.
# 7. Sondaje Minero:
# Diamantina: Extrae núcleos de roca para evaluar depósitos minerales.
# Circulación Reversa: Muestras fragmentadas para análisis preliminares en minería superficial.
# 8. Sondaje Sísmico:
# Sísmica de Reflexión: Usa ondas para mapear las estructuras geológicas.
# Sísmica de Refracción: Analiza las velocidades de ondas para identificar capas subterráneas.

#DIAMETROS
# Diámetros de Sondajes Consolidado
# Diamantina:
# AQ: 27 mm (núcleo) / 48 mm (externo).
# BQ: 36 mm / 60 mm.
# NQ: 47 mm / 75 mm.
# HQ: 63 mm / 96 mm.
# HQ3:
# PQ: 85 mm / 122 mm.
# PQ3

# Rotopercusión:
# Desde 3 pulgadas (76 mm) hasta 8 pulgadas (203 mm).

# Hidrogeológico:
# 2 pulgadas (51 mm): Para monitoreo.
# 4 pulgadas (102 mm): Usos básicos.
# 6 pulgadas (152 mm): Extracción moderada.
# 8-12 pulgadas o más (203-305 mm): Pozos de alta capacidad.


# Ambiental:
# Entre 2 y 6 pulgadas (51-152 mm).

# Geotécnico y de Cimentación:
# Perforaciones: 100-200 mm.

# Calicatas: 300-600 mm o más.

# Petrolero:
# 8,5 pulgadas (216 mm): Exploración inicial.
# 12,25 pulgadas (311 mm): Perforación intermedia.
# 17,5 pulgadas (445 mm) o mayores: Pozos grandes.

# Minero:
# Circulación Reversa (RC):
# 4,5 pulgadas (114 mm) para exploración superficial.
# 5 a 6 pulgadas (127-152 mm) para estudios más profundos.
# Diamantina: AQ, BQ, NQ, HQ, PQ.
# Ensayos In Situ:
# Calicatas: 300-600 mm.
# Excavaciones grandes: 800 mm o más.

# Muestreo ########################

from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
import logging

logger = logging.getLogger(__name__)

class MuestreoImage(models.Model):
    muestreo = models.ForeignKey('Muestreo', on_delete=models.CASCADE, related_name='muestreo_imagenes')
    image = models.ImageField(upload_to='muestreo_images/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f"Imagen de {self.muestreo.id_muestra}"


class Muestreo(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey('Prospecciones', on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion', related_name='muestreos_por_id')
    area = models.CharField(max_length=50, null=False, blank=False)
    fecha_muestreo = models.DateField(null=True, blank=True)
    objetivo = models.CharField(
        max_length=255,
        choices=[
            # ENSAYOS BÁSICOS Y CLASIFICACIÓN
            ('USCS', 'Clasificación completa (USCS)'),
            ('W', 'Humedad natural'),
            ('LIM', 'Límites'),
            ('GRA', 'Granulometría'),
            ('Gs', 'Peso específico de sólidos'),
            ('PF', 'Propiedades físicas (básicas)'),

            # COMPACTACIÓN Y DENSIDAD
            ('PM', 'Proctor modificado'),
            ('COMP', 'Proctor estándar'),
            ('DR', 'Densidad máxima y mínima'),
            ('DR_IN_SITU', 'Densidad in situ'),
            ('DR_APARENTE', 'Densidad aparente'),
            ('PU', 'Peso unitario'),

            # RESISTENCIA Y DEFORMACIÓN
            ('CBR', 'Capacidad de soporte CBR'),
            ('CS', 'Compresión simple'),
            ('CD', 'Corte directo'),
            ('TX15_6', 'Triaxial CIU/CID 15x30 (6kg/cm²)'),
            ('TX15_9', 'Triaxial CIU/CID 15x30 (9kg/cm²)'),
            ('TX10_6', 'Triaxial CIU/CID 10x20 (6kg/cm²)'),
            ('TX10_12', 'Triaxial CIU/CID 10x20 (12kg/cm²)'),
            ('TIB', 'Tracción indirecta (Brasileño)'),
            ('CP', 'Carga puntual (roca)'),
            ('IC', 'Índice de compresibilidad'),
            ('CV', 'Consolidación (Edómetro)'),

            # PERMEABILIDAD Y AGUA
            ('PER', 'Permeabilidad'),
            ('PPF_10x20', 'Permeabilidad pared flexible (10x20)'),
            ('PPF_15x30', 'Permeabilidad pared flexible (15x30)'),
            ('AA', 'Absorción de agua'),
            ('HL', 'Hinchamiento libre'),
            ('PHINCH', 'Presión de hinchamiento'),

            # QUÍMICOS Y DURABILIDAD
            ('SS', 'Sales solubles totales'),
            ('CL', 'Cloruros'),
            ('SULF', 'Sulfatos'),
            ('CARB', 'Carbonatos'),
            ('PH', 'pH'),
            ('ABA', 'Balance ácido'),
            ('NAG', 'Generación de ácido neutralizado'),
            ('DS', 'Desintegración por sulfatos'),
            ('SD', 'Slake durability'),
            ('LA', 'Desgaste Los Ángeles'),

            # GEOTÉCNICA ESPECIAL
            ('RE', 'Resistividad eléctrica'),
            ('MT', 'Metales traza'),
            ('SPLP', 'Lixiviación SPLP'),
            ('STLC', 'Límite umbral soluble (STLC)'),
            ('DRX', 'Difracción de rayos X'),
            ('EQ', 'Equivalente de arena'),

            # OPCIONALES/ADICIONALES
            ('CE', 'Contracción por secado'),
            ('IO', 'Impurezas orgánicas'),
            ('TX_DEF', 'Triaxial con deformación axial/transversal'),
        ],
        null=True, blank=True
    )
    id_bulto = models.CharField(max_length=255, null=True, blank=True)  # Embalaje del bulto, ejemplo P-1
    tipo_bulto = models.CharField(
        max_length=25,
        choices=[
            ('pallets', 'Pallets'),
            ('caja_varias_muestras', 'Caja (para varias muestras)'),
            ('bins', 'Bins'),
            ('tambor', 'Tambor'),
            ('otro', 'Otro'),
        ],
        null=True,
        blank=True
    )
    id_embalaje_muestra = models.CharField(max_length=255, null=True, blank=True)  # Embalaje de la muestra, ejemplo C-1
    tipo_embalaje_muestra = models.CharField(
        max_length=25,
        choices=[
            ('caja_testigos', 'Caja testigos'),
            ('bolsa_muestra', 'Bolsa muestra'),
            ('saco_muestra', 'Saco muestra'),
            ('tubo_pvc', 'Tubo PVC'),
            ('otro', 'Otro'),
        ],
        null=True,
        blank=True
    )
    id_muestra = models.CharField(max_length=50, null=False, blank=False)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    peso_unitario = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    peso_total = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    profundidad_desde = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    profundidad_hasta = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    profundidad_promedio = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    espesor_estrato = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estrato = models.CharField(
        max_length=25,
        choices=[
            ('h1', 'H1'),
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
            ('h5', 'H5'),
            ('h6', 'H6'),
            ('h7', 'H7'),
            ('h8', 'H8'),
        ],
        null=True,
        blank=True
    )
    tipo = models.CharField(
        max_length=25,
        choices=[
            ('perturbada', 'Perturbada'),
            ('no_perturbada', 'No perturbada'),
            ('colpa', 'Colpa'),
        ],
        null=True,
        blank=True
    )
    fecha_despacho = models.DateField(null=True, blank=True)
    nombre_despachador = models.CharField(max_length=50, null=True, blank=True)
    destino = models.CharField(max_length=50, null=True, blank=True)
    orden_transporte = models.CharField(max_length=50, null=True, blank=True)
    observacion = models.CharField(max_length=255, null=True, blank=True)
    id_laboratorio = models.CharField(max_length=255, null=True, blank=True)  # Generado como id_prospeccion_id_muestra_objetivo
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    imagenes = models.ManyToManyField('MuestreoImage', blank=True, related_name='muestreos_con_imagen')
    history = HistoricalRecords()

    class Meta:
        db_table = 'muestreo'

    def save(self, *args, **kwargs):
        # Generar id_laboratorio si no está definido manualmente
        if not self.id_laboratorio and self.id_prospeccion and self.id_muestra and self.objetivo:
            self.id_laboratorio = f"{self.id_prospeccion.id_prospeccion}_{self.id_muestra}_{self.objetivo}"
        # Cálculos existentes
        if self.peso_unitario and self.cantidad:
            self.peso_total = self.peso_unitario * self.cantidad
        if self.profundidad_desde is not None and self.profundidad_hasta is not None:
            self.profundidad_promedio = (self.profundidad_desde + self.profundidad_hasta) / 2
            self.espesor_estrato = self.profundidad_hasta - self.profundidad_desde
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prospección: {self.id_prospeccion.id_prospeccion}, Muestra: {self.id_muestra}, Embalaje: {self.id_embalaje_muestra or 'Sin embalaje'}"

# Programa ########################
logger = logging.getLogger(__name__)
class Programa(models.Model):
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    objetivo = models.CharField(max_length=255, choices=[
        ('clasificacion completa', 'Clasificación completa'),
        ('humedad', 'Humedad'),
        ('sales solubles, cloruros y sulfatos', 'Sales solubles, cloruros y sulfatos'),
        ('carbonatos', 'Carbonatos'),
        ('triaxial ciu/cid 15x30 hasta 6kg cm2', 'Triaxial CIU/CID 15x30 hasta 6kg/cm²'),
        ('triaxial ciu/cid 15x30 hasta 9kg cm2', 'Triaxial CIU/CID 15x30 hasta 9kg/cm²'),
        ('granulometria', 'Granulometría'),
        ('peso unitario', 'Peso unitario'),
        ('difraccion de rayos x', 'Difracción de rayos X'),
        ('triaxial ciu/cid 5x10 hasta 6kg cm2', 'Triaxial CIU/CID 5x10 hasta 6kg/cm²'),
        ('triaxial ciu/cid 5x10 hasta 30kg cm2', 'Triaxial CIU/CID 5x10 hasta 30kg/cm²'),
        ('impurezas organicas', 'Impurezas orgánicas'),
        ('sales solubles totales', 'Sales solubles totales'),
        ('resistencia al desgaste, metodo los angeles', 'Resistencia al desgaste, método Los Ángeles'),
        ('densidad in situ', 'Densidad in situ'),
        ('densidad aparente', 'Densidad aparente'),
        ('resistencia a la desintegracion', 'Resistencia a la desintegración'),
        ('uscs', 'USCS'),
        ('triaxial ciu/cid 10x20 hasta 6kg cm2', 'Triaxial CIU/CID 10x20 hasta 6kg/cm²'),
        ('triaxial ciu/cid 10x20 hasta 12kg cm2', 'Triaxial CIU/CID 10x20 hasta 12kg/cm²'),
        ('densidad maxima y minima', 'Densidad máxima y mínima'),
        ('permeabilidad pared flexible carga constante (10x20 hasta 6 kg/cm2)', 'Permeabilidad pared flexible carga constante (10x20 hasta 6 kg/cm²)'),
        ('permeabilidad pared flexible carga constante (15x30 hasta 6 kg/cm2)', 'Permeabilidad pared flexible carga constante (15x30 hasta 6 kg/cm²)'),
        ('cbr', 'CBR'),
        ('slake durability', 'Slake durability'),
        ('proctor modificado', 'Proctor modificado'),
        ('corte directo', 'Corte directo'),
        ('ph', 'pH'),
        ('determinacion de propiedades fisicas', 'Determinación de propiedades físicas'),
        ('resistividad electrica', 'Resistividad eléctrica'),
        ('compresion simple', 'Compresión simple'),
        ('carga puntual', 'Carga puntual'),
        ('traccion indirecta, metodo brasileno', 'Tracción indirecta, método brasileño'),
        ('triaxial con medicion de deformacion axial y transversal', 'Triaxial con medición de deformación axial y transversal'),
    ], null=True, blank=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha_ingreso_lab = models.DateField(null=True, blank=True)
    id_ingreso = models.CharField(max_length=50, null=False, blank=False)
    area = models.CharField(max_length=50, null=False, blank=False)
    fecha_envio_programa = models.DateField(null=True, blank=True)
    asignar_muestra = models.CharField(max_length=50, null=True, blank=True)
    fecha_informe = models.DateField(null=True, blank=True)
    cantidad_recibida = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    n_informe = models.CharField(max_length=50, null=True, blank=True)
    n_ep = models.CharField(max_length=50, null=True, blank=True)
    observacion = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'programa'

    def __str__(self):
        return f"Programa: {self.id_proyecto.id} - {self.objetivo}"


# Ejemplo de estructura de modelo
# logger = logging.getLogger(__name__)
# class uscs(models.Model):
#     id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
#     tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
#     id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
#     area = models.CharField(max_length=50, null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     history = HistoricalRecords()


####ENSAYOS INSITU##
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
import logging

####ENSAYOS INSITU##
logger = logging.getLogger(__name__)
class densidad_insitu(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', on_delete=models.CASCADE, db_column='id_proyecto', to_field='id') #utiliza la misma escructura que en humedad (replica)
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True) #utiliza la misma escructura que en humedad (replica)
    id_prospeccion = models.ForeignKey('Prospecciones', on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion') #utiliza la misma escructura que en humedad (replica)
    id_muestra = models.CharField(max_length=50, null=False, blank=False) #Este va a quedar como una lista desplegale al igual que "id_proyecto, tipo_prospeccion, id_prospeccion"
    profundidad_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_promedio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    profundidad_ensayo = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    horizonte = models.CharField(max_length=50, null=True, blank=True)  #Averiguar bien la calsificacion, se indica en uno que es H-1 pero deberia corrsponder al estrato.. revisar

    #desde aqui calcular lo que corrsponda
    cota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    profundidad_nivel_freatico = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    condicion_ambiental = models.CharField(max_length=50, null=True, blank=True)
    peso_materia_humedo = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) # en gramos (g)
    masa_arena_inicial_en_cono_superior = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) # en gramos (g)
    masa_arena_remanente_en_cono_superior = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) #en gramos (g)
    masa_arena_en_cono_inferior = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) #en gramos (g)
    masa_arena_excavacion = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) # (masa_arena_inicial_en_cono_superior - masa_arena_remanente_en_cono_superior_(g) - masa_arena_en_cono_inferior) en gramos (g)
    densidad_aparente_arena = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) # en (g/cm3)
    volumen_perforacion = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) # (masa_arena_excavacion / densidad_aparente_arena_ensayo) en (cm3)
    densidad_natural_del_suelo = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)  #(peso_materia_húmedo / volumen_de_la_perforación) en (g/cm3)

    peso_suelo_humedo = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) #en gramos
    peso_suelo_seco = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) #en gramos
    peso_agua = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) # (peso_suelo_húmedo - peso_suelo_seco) en gramos (g)
    humedad = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) # ((peso_agua / peso_suelo_seco) * 100) en (%)

    densidad_seca_del_suelo = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)  #(densidad_natural_del_suelo / (1 + (humedad / 100))) en (g/cm3)


    area = models.CharField(max_length=50, null=True, blank=True)
    observacion = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()


    class Meta:
        db_table = 'densidad_insitu'

    def save(self, *args, **kwargs):
        if self.masa_arena_inicial_en_cono_superior is not None and \
           self.masa_arena_remanente_en_cono_superior is not None and \
           self.masa_arena_en_cono_inferior is not None:
            self.masa_arena_excavacion = self.masa_arena_inicial_en_cono_superior - self.masa_arena_remanente_en_cono_superior - self.masa_arena_en_cono_inferior

        if self.masa_arena_excavacion is not None and self.densidad_aparente_arena is not None:
            self.volumen_perforacion = self.masa_arena_excavacion / self.densidad_aparente_arena

        if self.peso_materia_humedo is not None and self.volumen_perforacion is not None:
            self.densidad_natural_del_suelo = self.peso_materia_humedo / self.volumen_perforacion

        if self.peso_suelo_humedo is not None and self.peso_suelo_seco is not None:
            self.peso_agua = self.peso_suelo_humedo - self.peso_suelo_seco

        if self.peso_agua is not None and self.peso_suelo_seco is not None and self.peso_suelo_seco != 0:
            self.humedad = (self.peso_agua / self.peso_suelo_seco) * 100
        elif self.peso_agua is not None and self.peso_suelo_seco == 0:
            self.humedad = 0  # Evitar división por cero

        if self.densidad_natural_del_suelo is not None and self.humedad is not None:
            self.densidad_seca_del_suelo = self.densidad_natural_del_suelo / (1 + (self.humedad / 100))

        super().save(*args, **kwargs)
        

####ENSAYOS LABORATORIO##

# Clasificacion USC ########################
logger = logging.getLogger(__name__)
class uscs(models.Model):
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id') #utiliza la misma escructura que en humedad (replica)
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True) #utiliza la misma escructura que en humedad (replica)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion') #utiliza la misma escructura que en humedad (replica)
    id_muestra = models.CharField(max_length=50, null=False, blank=False) #Este va a quedar como una lista desplegale al igual que "id_proyecto, tipo_prospeccion, id_prospeccion"
    profundidad_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_promedio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    uscs = models.CharField(max_length=255, choices=[
        ('CL', 'CL'),
        ('GM', 'GM'),
        ('GP', 'GP'),
        ('GP-GC', 'GP-GC'),
        ('GP-GM', 'GP-GM'),
        ('GW-GM', 'GW-GM'),
        ('GW', 'GW'),
        ('GW-GC', 'GW-GC'),
        ('GC', 'GC'),
        ('GC-GM', 'GC-GM'),
        ('SC', 'SC'),
        ('SC-SM', 'SC-SM'),
        ('SP', 'SP'),
        ('SP-SC', 'SP-SC'),
        ('SP-SM', 'SP-SM'),
        ('SW', 'SW'),
        ('SW-SC', 'SW-SC'),
        ('SW-SM', 'SW-SM'),
        ('ML', 'ML'),
        ('MH', 'MH'),
        ('RC', 'RC'),
        ('SM', 'SM'),
        ('CL-ML', 'CL-ML'),
        ('CH', 'CH'),
        ('OL', 'OL'),
        ('OH', 'OH'),
        ('PT', 'PT'),
    ], null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True) 
    observacion = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()


    class Meta:
        db_table = 'uscs'

# Indice de plasticidad (limites de atterberg) ########################
# Indice de plasticidad (limites de atterberg) ########################
logger = logging.getLogger(__name__)

class Limites_atterberg(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey('Prospecciones', on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    id_muestra = models.CharField(max_length=50, null=False, blank=False)
    profundidad_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    profundidad_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    profundidad_promedio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    limite_liquido = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    limite_plastico = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    indice_plasticidad = models.CharField(max_length=10, null=True, blank=True)
    metodo = models.CharField(max_length=50, null=True, blank=True)
    acanalado = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    observacion = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Corrección aquí
    history = HistoricalRecords()

    class Meta:
        db_table = 'Limites_atterberg'

    def clean(self):
        super().clean()
        if self.indice_plasticidad:
            try:
                decimal_value = float(self.indice_plasticidad)
            except ValueError:
                pass


#DEFINICIO DE NP
#En el contexto de los límites de Atterberg y la clasificación de suelos, NP significa No Plástico.
#Un suelo se clasifica como no plástico (NP) si no tiene un límite plástico (PL) ni un límite líquido (LL) definidos. 
# Esto significa que el suelo no muestra una transición clara entre los estados sólido, semisólido, plástico y líquido con diferentes contenidos de agua. 
# En otras palabras, el suelo no se comporta de manera plástica y no se puede moldear o deformar sin romperse.



# Gravedad especifica ########################
logger = logging.getLogger(__name__)
class gravedad_especifica(models.Model):
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id') #utiliza la misma escructura que en humedad (replica)
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True) #utiliza la misma escructura que en humedad (replica)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion') #utiliza la misma escructura que en humedad (replica)
    id_muestra = models.CharField(max_length=50, null=False, blank=False) #Este va a quedar como una lista desplegale al igual que "id_proyecto, tipo_prospeccion, id_prospeccion"
    profundidad_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_promedio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    gravedad_especifica = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True) 
    observacion = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'gravedad_especifica'


# Granulometria ########################
logger = logging.getLogger(__name__)
class Granulometria(models.Model):
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    id_muestra = models.CharField(max_length=50, null=False, blank=False) #Este va a quedar como una lista desplegale al igual que "id_proyecto, tipo_prospeccion, id_prospeccion"
    profundidad_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_promedio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    area = models.CharField(max_length=50, null=True, blank=True)
    n_0075 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)  
    n_0110 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)  
    n_0250 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)  
    n_0420 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True) 
    n_0840 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)  
    n_2000 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)  
    n_4760 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)  
    n_9520 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)  
    n_19000 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True) 
    n_25400 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True) 
    n_38100 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True) 
    n_50800 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True) 
    n_63500 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True) 
    n_75000 = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    observacion = models.CharField(max_length=255, null=False) 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'granulometria'

    def __str__(self):
        return f"Granulometría: {self.id_prospeccion.id_prospeccion}"


#CBR «California Bearing Ratio»
logger = logging.getLogger(__name__)
class Cbr(models.Model):
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    id_muestra = models.CharField(max_length=50, null=False, blank=False) #Este va a quedar como una lista desplegale al igual que "id_proyecto, tipo_prospeccion, id_prospeccion"
    profundidad_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_promedio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    area = models.CharField(max_length=50, null=True, blank=True)
    densidad_seca_ai = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Densidad Seca (g/cm3) Antes de la inmersión (ai)
    densidad_seca_di = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  #Densidad Seca (g/cm3) Antes de la inmersión (di)
    humedad_ai = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #(%) Antes de la inmersión
    humedad_di = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #(%) Despues de la inmersión
    cbr_01 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # (%)
    cbr_02 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # (%)
    observacion = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'cbr'

    def __str__(self):
        return f"cbr: {self.id_prospeccion.id_prospeccion}"

#El CBR es un ensayo para evaluar la calidad del un material de suelo con base en su resistencia, medida a través de un ensayo de placa a escala.
#CBR significa en español relación de soporte California, por las siglas en inglés de «California Bearing Ratio», aunque en países como México se conoce también este ensayo por las siglas VRS, de Valor Relativo del Soporte.



# Humedad ########################
logger = logging.getLogger(__name__)
class Humedad(models.Model):
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    id_muestra = models.CharField(max_length=50, null=False, blank=False) #Este va a quedar como una lista desplegale al igual que "id_proyecto, tipo_prospeccion, id_prospeccion"
    area = models.CharField(max_length=50, null=True, blank=True)
    humedad = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    profundidad_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Deben solicitidar al modelo muestreo y cargarse automaticamente, sin modificacion al igual que area
    profundidad_promedio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    observacion = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'humedad'

    def __str__(self):
        return f"Humedad: {self.id_prospeccion.id_prospeccion} - {self.humedad}%"



# Area ########################
class Area(models.Model):
    nombre = models.CharField(max_length=255)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, to_field='id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'area'

    def __str__(self):
        return f"Área: {self.nombre} - {self.proyecto.id}"





#############JORNADA#######################
logger = logging.getLogger(__name__)
class JornadaTeorica(models.Model):
    TIPO_JORNADA = (
        ('4x3', '4x3 Excepcional'),
        ('5x2', '5x2 Ordinaria'),
        ('8x6', '8x6 Bisemanal'),
        ('7x7', '7x7 Excepcional'),
        ('10x10', '10x10 Excepcional'),
        ('14x14', '14x14 Excepcional'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_JORNADA, unique=True, help_text="Tipo de jornada laboral")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()  
    dias_trabajados = models.DecimalField(max_digits=4, decimal_places=1, help_text="Días trabajados en el ciclo")
    dias_descanso = models.DecimalField(max_digits=4, decimal_places=1, help_text="Días de descanso en el ciclo")
    colacion = models.DecimalField(max_digits=4, decimal_places=2, help_text="Horas de colación diarias")
    horas_legales_diarias = models.DecimalField(max_digits=5, decimal_places=2, help_text="Horas legales diarias")
    horas_totales_diarias = models.DecimalField(max_digits=5, decimal_places=2, help_text="Horas totales diarias")
    horas_efectivas_diarias = models.DecimalField(max_digits=5, decimal_places=2, help_text="Horas efectivas diarias")
    horas_semanales_legales = models.DecimalField(max_digits=5, decimal_places=2, help_text="Horas semanales legales")
    horas_semanales_totales = models.DecimalField(max_digits=5, decimal_places=2, help_text="Horas semanales totales")
    horas_semanales_efectivas = models.DecimalField(max_digits=5, decimal_places=2, help_text="Horas semanales efectivas")
    horas_mensuales_legales = models.DecimalField(max_digits=6, decimal_places=2, help_text="Horas mensuales legales")
    horas_mensuales_totales = models.DecimalField(max_digits=6, decimal_places=2, help_text="Horas mensuales totales")
    horas_mensuales_efectivas = models.DecimalField(max_digits=6, decimal_places=2, help_text="Horas mensuales efectivas")
    colacion_tipo = models.CharField(
        max_length=20,
        choices=[('imputable', 'Imputable a la jornada'), ('no_imputable', 'No imputable a la jornada'), ('sin_colacion', 'Sin colación')],
        help_text="Tipo de colación"
    )

    class Meta:
        indexes = [models.Index(fields=['tipo'])]

    def __str__(self):
        return dict(self.TIPO_JORNADA).get(self.tipo, self.tipo)

    @staticmethod
    def populate_initial_data():
        jornadas = [
            {
                'tipo': '4x3',
                'dias_trabajados': Decimal('4.0'),
                'dias_descanso': Decimal('3.0'),
                'colacion': Decimal('1.0'),
                'horas_legales_diarias': Decimal('10.0'),
                'horas_totales_diarias': Decimal('11.0'),
                'horas_efectivas_diarias': Decimal('10.0'),
                'horas_semanales_legales': Decimal('40.0'),
                'horas_semanales_totales': Decimal('44.0'),
                'horas_semanales_efectivas': Decimal('40.0'),
                'horas_mensuales_legales': Decimal('173.2'),
                'horas_mensuales_totales': Decimal('190.5'),
                'horas_mensuales_efectivas': Decimal('173.2'),
                'colacion_tipo': 'no_imputable'
            },
            {
                'tipo': '5x2',
                'dias_trabajados': Decimal('5.0'),  # Total L-J (4) + V (1)
                'dias_descanso': Decimal('2.0'),    # Sábado y domingo
                'colacion': Decimal('0.4'),         # Promedio: (0.5*4 + 0*1)/5
                'horas_legales_diarias': Decimal('8.0'),  # Promedio: (8.5*4 + 6.0*1)/5 = 8.0
                'horas_totales_diarias': Decimal('8.4'),  # Promedio: (9.0*4 + 6.0*1)/5 = 8.4
                'horas_efectivas_diarias': Decimal('8.0'),  # Promedio: (8.5*4 + 6.0*1)/5 = 8.0
                'horas_semanales_legales': Decimal('40.0'),  # 34.0 (L-J) + 6.0 (V)
                'horas_semanales_totales': Decimal('42.0'),  # 36.0 (L-J) + 6.0 (V)
                'horas_semanales_efectivas': Decimal('40.0'),  # 34.0 (L-J) + 6.0 (V)
                'horas_mensuales_legales': Decimal('173.26'),  # 147.22 (L-J) + 26.04 (V)
                'horas_mensuales_totales': Decimal('181.92'),  # 155.88 (L-J) + 26.04 (V)
                'horas_mensuales_efectivas': Decimal('173.26'),  # 147.22 (L-J) + 26.04 (V)
                'colacion_tipo': 'no_imputable'
            },
            {
                'tipo': '8x6',
                'dias_trabajados': Decimal('8.0'),
                'dias_descanso': Decimal('6.0'),
                'colacion': Decimal('1.0'),
                'horas_legales_diarias': Decimal('10.0'),
                'horas_totales_diarias': Decimal('11.0'),
                'horas_efectivas_diarias': Decimal('10.0'),  # Actualizado de 9.0 a 10.0
                'horas_semanales_legales': Decimal('40.0'),
                'horas_semanales_totales': Decimal('44.0'),
                'horas_semanales_efectivas': Decimal('40.0'),  # Actualizado de 36.0 a 40.0
                'horas_mensuales_legales': Decimal('173.2'),
                'horas_mensuales_totales': Decimal('190.5'),   # Actualizado de 190.52 a 190.5
                'horas_mensuales_efectivas': Decimal('173.2'),   # Actualizado de 155.88 a 173.2
                'colacion_tipo': 'no_imputable'
            },
            {
                'tipo': '7x7',
                'dias_trabajados': Decimal('7.0'),
                'dias_descanso': Decimal('7.0'),
                'colacion': Decimal('1.0'),
                'horas_legales_diarias': Decimal('12.0'),
                'horas_totales_diarias': Decimal('12.0'),
                'horas_efectivas_diarias': Decimal('11.0'),
                'horas_semanales_legales': Decimal('42.0'),
                'horas_semanales_totales': Decimal('42.0'),
                'horas_semanales_efectivas': Decimal('38.5'),
                'horas_mensuales_legales': Decimal('181.86'),
                'horas_mensuales_totales': Decimal('181.86'),
                'horas_mensuales_efectivas': Decimal('166.31'),
                'colacion_tipo': 'imputable'
            },
            {
                'tipo': '10x10',
                'dias_trabajados': Decimal('10.0'),
                'dias_descanso': Decimal('10.0'),
                'colacion': Decimal('1.0'),
                'horas_legales_diarias': Decimal('12.0'),
                'horas_totales_diarias': Decimal('12.0'),
                'horas_efectivas_diarias': Decimal('11.0'),
                'horas_semanales_legales': Decimal('42.0'),
                'horas_semanales_totales': Decimal('42.0'),
                'horas_semanales_efectivas': Decimal('38.5'),
                'horas_mensuales_legales': Decimal('181.86'),
                'horas_mensuales_totales': Decimal('181.86'),
                'horas_mensuales_efectivas': Decimal('166.31'),
                'colacion_tipo': 'imputable'
            },
            {
                'tipo': '14x14',
                'dias_trabajados': Decimal('14.0'),
                'dias_descanso': Decimal('14.0'),
                'colacion': Decimal('1.0'),
                'horas_legales_diarias': Decimal('12.0'),
                'horas_totales_diarias': Decimal('12.0'),
                'horas_efectivas_diarias': Decimal('11.0'),
                'horas_semanales_legales': Decimal('42.0'),
                'horas_semanales_totales': Decimal('42.0'),
                'horas_semanales_efectivas': Decimal('38.5'),
                'horas_mensuales_legales': Decimal('181.86'),
                'horas_mensuales_totales': Decimal('181.86'),
                'horas_mensuales_efectivas': Decimal('166.31'),
                'colacion_tipo': 'imputable'
            },
        ]
        for data in jornadas:
            JornadaTeorica.objects.get_or_create(tipo=data['tipo'], defaults=data)
            logger.info(f"Jornada inicial creada o verificada: {data['tipo']}") 
   


#Nomina############################################
logger = logging.getLogger(__name__)
class Nomina(models.Model):
    id_proyecto = models.ForeignKey('Proyectos', on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    empresa = models.CharField(max_length=25, null=False)
    fecha_ingreso = models.DateField(null=True, blank=True)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    rut = models.CharField(max_length=25, null=False, unique=True)
    email = models.CharField(max_length=50, null=False)
    telefono = models.CharField(max_length=15, null=False)
    cargo = models.CharField(max_length=25, null=False)
    titulo = models.CharField(max_length=25, null=False)
    turno = models.CharField(max_length=25, choices=[
        ('4x3 excepcional', '4x3 excepcional'),
        ('5x2 ordinaria', '5x2 ordinaria'),
        ('8x6 bisemanal', '8x6 bisemanal'),
        ('7x7 excepcional', '7x7 excepcional'),
        ('10x10 excepcional', '10x10 excepcional'),
        ('14x14 excepcional', '14x14 excepcional'),
    ], null=True, blank=True)
    ultimo_dia = models.DateField(null=True, blank=True)
    primer_dia = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    horas_por_dia_lista = models.JSONField(null=True, blank=True)
    total_horas = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    horas_semanales = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    horas_mensuales = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    def get_jornada_teorica(self):
        if not self.turno:
            logger.error(f"No se especificó turno para la nómina {self.id}")
            return None
        turno_mapping = {
            '4x3 excepcional': '4x3',
            '5x2 ordinaria': '5x2',
            '8x6 bisemanal': '8x6',
            '7x7 excepcional': '7x7',
            '10x10 excepcional': '10x10',
            '14x14 excepcional': '14x14',
        }
        tipo_jornada = turno_mapping.get(self.turno)
        if not tipo_jornada:
            logger.error(f"No se encontró mapeo para el turno '{self.turno}' en la nómina {self.id}")
            return None
        jornada = JornadaTeorica.objects.filter(tipo=tipo_jornada).first()
        if not jornada:
            logger.error(f"No se encontró jornada teórica para el tipo '{tipo_jornada}' en la nómina {self.id}")
        return jornada

    def get_hours_for_date(self, date):
        jornada = self.get_jornada_teorica()
        if not jornada:
            return 0.0
        if self.turno == '5x2 ordinaria':
            # Lunes a jueves: 8.5 horas legales, viernes: 6.0 horas legales, sábado y domingo: 0.0
            if date.weekday() < 4:  # Lunes a Jueves (0-3)
                return 8.5  # Horas legales diarias para L-J
            elif date.weekday() == 4:  # Viernes (4)
                return 6.0  # Horas legales diarias para V
            else:  # Sábado y Domingo (5, 6)
                return 0.0
        elif self.turno == '4x3 excepcional':
            # Lunes a Jueves: 10.0 horas legales, viernes a domingo: 0.0
            if date.weekday() < 4:  # Lunes a Jueves (0-3)
                return float(jornada.horas_legales_diarias)  # 10.0 horas
            else:
                return 0.0
        elif self.turno in ['7x7 excepcional', '10x10 excepcional', '14x14 excepcional', '8x6 bisemanal']:
            # Ciclo de trabajo y descanso basado en primer_dia
            cycle_lengths = {
                '7x7 excepcional': int(jornada.dias_trabajados + jornada.dias_descanso),
                '10x10 excepcional': int(jornada.dias_trabajados + jornada.dias_descanso),
                '14x14 excepcional': int(jornada.dias_trabajados + jornada.dias_descanso),
                '8x6 bisemanal': int(jornada.dias_trabajados + jornada.dias_descanso),
            }
            work_days = int(jornada.dias_trabajados)
            cycle_length = cycle_lengths.get(self.turno, 14)
            days_since_start = (date - self.primer_dia).days
            day_in_cycle = days_since_start % cycle_length
            if day_in_cycle < work_days:
                return float(jornada.horas_legales_diarias)  # Usar horas legales
            else:
                return 0.0
        return 0.0

    def generar_rango_fechas(self, inicio, fin):
        return [inicio + timedelta(days=i) for i in range((fin - inicio).days + 1)]

    def generar_roster_para_nomina(self):
        fecha_inicio = self.primer_dia or self.fecha_ingreso or date.today()
        fecha_fin = self.ultimo_dia or fecha_inicio + timedelta(days=30)
        fechas = self.generar_rango_fechas(fecha_inicio, fecha_fin)
        logger.info(f"Generando roster para nómina {self.id}. Rango: {fecha_inicio} a {fecha_fin}")
        self.rosters.all().delete()
        horas_por_dia = []
        for dia in fechas:
            horas = self.get_hours_for_date(dia)
            Roster.objects.create(nomina=self, fecha=dia, horas_asignadas=Decimal(str(horas)))
            horas_por_dia.append(horas)
            logger.debug(f"Día {dia}: {horas} horas legales asignadas")
        self.horas_por_dia_lista = horas_por_dia
        self.total_horas = Decimal(str(sum(horas_por_dia)))

        # Calcular horas semanales según el turno (basado en horas legales)
        if self.turno == '5x2 ordinaria':
            self.horas_semanales = Decimal('40.0')  # 34.0 (L-J: 8.5*4) + 6.0 (V)
        elif self.turno in ['7x7 excepcional', '10x10 excepcional', '14x14 excepcional', '8x6 bisemanal']:
            jornada = self.get_jornada_teorica()
            work_days = int(jornada.dias_trabajados)
            cycle_hours = [self.get_hours_for_date(fechas[i]) for i in range(min(work_days, len(fechas)))]
            self.horas_semanales = Decimal(str(sum(cycle_hours[:7])))  # Primeros 7 días del ciclo
        else:
            self.horas_semanales = Decimal(str(sum(horas_por_dia[:7])))

        # Calcular horas mensuales según el turno (basado en horas legales)
        if self.turno == '5x2 ordinaria':
            self.horas_mensuales = Decimal('173.26')  # 147.22 (L-J) + 26.04 (V)
        else:
            self.horas_mensuales = Decimal(str(sum(horas_por_dia)))
        self.save()
        logger.info(f"Roster generado: Total horas {self.total_horas}, Semanales {self.horas_semanales}, Mensuales {self.horas_mensuales}")

logger = logging.getLogger(__name__)
class Roster(models.Model):
    nomina = models.ForeignKey(Nomina, on_delete=models.CASCADE, related_name='rosters')
    fecha = models.DateField()
    horas_asignadas = models.DecimalField(max_digits=5, decimal_places=2)
    history = HistoricalRecords()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  

    class Meta:
        indexes = [
            models.Index(fields=['nomina', 'fecha']),
            models.Index(fields=['fecha']),
        ]
        unique_together = ('nomina', 'fecha')
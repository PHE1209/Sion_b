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



"""
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
"""

# Tablas de ejemplo (sin cambios)
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)



# Proyectos ########################
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

    class Meta:
        db_table = 'proyecto_usuario'
        unique_together = ('proyecto', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} - {self.proyecto.id} ({self.rol})"


# Prospecciones ########################
class Prospecciones(models.Model):
    tipo_prospeccion = models.CharField(max_length=25, choices=[
        ('sondajes', 'Sondajes'),
        ('calicatas', 'Calicatas'),
        ('geofisica', 'Geofísica'),
    ], null=False)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    id_prospeccion = models.CharField(max_length=25, null=False, unique=True)  # Sin restricción de formato
    area = models.CharField(max_length=50, null=False, blank=False, default='')
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    coordenada_este = models.CharField(max_length=20, null=True, blank=True)
    coordenada_norte = models.CharField(max_length=20, null=True, blank=True)
    elevacion = models.IntegerField(null=True, blank=True)
    profundidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    observacion = models.CharField(max_length=255, null=True, blank=True)
    verificacion_puntos = models.CharField(max_length=25, choices=[
        ('realizado', 'Realizado'),
        ('no_realizado', 'No Realizado'),
    ], null=True, blank=True)
    plataforma = models.CharField(max_length=25, choices=[
        ('realizado', 'Realizado'),
        ('no_realizado', 'No Realizado'),
    ], null=True, blank=True)
    inclinacion = models.IntegerField(null=True, blank=True)
    diametro = models.IntegerField(null=True, blank=True)
    tapado = models.CharField(max_length=25, choices=[
        ('si', 'Sí'),
        ('no', 'No'),
    ], null=True, blank=True)
    contratista = models.CharField(max_length=100, null=True, blank=True)
    marca_maquina1 = models.CharField(max_length=50, null=True, blank=True)
    modelo_maquina1 = models.CharField(max_length=50, null=True, blank=True)
    ppu1 = models.CharField(max_length=10, null=True, blank=True)
    marca_maquina2 = models.CharField(max_length=50, null=True, blank=True)
    modelo_maquina2 = models.CharField(max_length=50, null=True, blank=True)
    ppu2 = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'prospecciones'

    def __str__(self):
        return self.id_prospeccion



# Muestreo ########################
class Muestreo(models.Model):
    id_embalaje = models.CharField(max_length=255, null=False, blank=False)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion', related_name='muestreos_por_id')
    area = models.CharField(max_length=50, null=False, blank=False)
    fecha_muestreo = models.DateField(null=True, blank=True)
    tipo_embalaje = models.CharField(max_length=25, choices=[
        ('caja_nucleo', 'Caja núcleo'),
        ('bolsa_muestra', 'Bolsa muestra'),
        ('saco_muestra', 'Saco muestra'),
        ('tubo_pvc', 'Tubo PVC'),
        ('tambor', 'Tambor'),
    ], null=True, blank=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    peso_unitario = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    peso_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    id_muestra = models.CharField(max_length=50, null=False, blank=False)
    profundidad_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    profundidad_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estrato = models.CharField(max_length=25, choices=[
        ('h1', 'H1'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6'),
        ('h7', 'H7'),
        ('h8', 'H8'),
    ], null=True, blank=True)
    tipo = models.CharField(max_length=25, choices=[
        ('perturbada', 'Perturbada'),
        ('no_perturbada', 'No perturbada'),
        ('colpa', 'Colpa'),
    ], null=True, blank=True)
    fecha_despacho = models.DateField(null=True, blank=True)
    nombre_despachador = models.CharField(max_length=50, null=True, blank=True)
    destino = models.CharField(max_length=50, null=True, blank=True)
    orden_transporte = models.CharField(max_length=50, null=True, blank=True)
    observacion = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'muestreo'

    def save(self, *args, **kwargs):
        if self.peso_unitario and self.cantidad:
            self.peso_total = self.peso_unitario * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prospección: {self.id_prospeccion.id_prospeccion}, Muestra: {self.id_muestra}, Embalaje: {self.id_embalaje}"



# Programa ########################
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'programa'

    def __str__(self):
        return f"Programa: {self.id_proyecto.id} - {self.objetivo}"



# Humedad ########################
class Humedad(models.Model):
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    humedad = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    profundidad_promedio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    area = models.CharField(max_length=50, null=True, blank=True)
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
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



# Granulometria ########################
class Granulometria(models.Model):
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    n_0075 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_0110 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_0250 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_0420 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_0840 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_2000 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_4760 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_9520 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_19000 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_25400 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_38100 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_50800 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_63500 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    n_75000 = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    area = models.CharField(max_length=50, null=True, blank=True)
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'granulometria'

    def __str__(self):
        return f"Granulometría: {self.id_prospeccion.id_prospeccion}"




#############JORNADA#######################
import logging
from decimal import Decimal
from django.db import models
import logging
from decimal import Decimal
from django.db import models

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

from datetime import timedelta, date
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

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

class Roster(models.Model):
    nomina = models.ForeignKey(Nomina, on_delete=models.CASCADE, related_name='rosters')
    fecha = models.DateField()
    horas_asignadas = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['nomina', 'fecha']),
            models.Index(fields=['fecha']),
        ]
        unique_together = ('nomina', 'fecha')
from mailbox import NoSuchMailboxError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
import json
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords


"""
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
"""
##  Tablas generalmente en ejercicios
##  como no tiene Meta(db_table), 
##   todas quedan con un prefijo
class Poll(models.Model):
    # No Tiene ID, es automático
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    # No tiene Id, es automático
    # Observe la FK, obligación => on_delete
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # Integer
    votes = models.IntegerField(default=0)

########################


class Usuarios(models.Model):
    n = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=25, null = False)
    nombre = models.CharField(max_length=50, null = False)
    apellido = models.CharField(max_length=50, null = False)
    email = models.CharField(max_length=50, null = False)
    telefono = models.CharField(max_length=15, null=False)
    class Meta:
        db_table = 'usuarios'


#Proyectos########################
#modelo proyectos (tabla)
class Proyectos(models.Model):
    n = models.AutoField(primary_key=True)
    estatus_proyecto = models.CharField(max_length=25, choices=[
        ('propuesta', 'Propuesta'),
        ('ejecucion', 'ejecucion'),
        ('standby', 'StandBy'),
    ], null=True    )
    id = models.CharField(max_length=25, null=False, unique=True)  # Asegurando unicidad en el campo id
    pm = models.CharField(max_length=50, null=False)
    empresa = models.CharField(max_length=50, null=False)
    nombre = models.CharField(max_length=255, null=False)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    alcance = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuario que realiza la operación

    class Meta:
        db_table = 'proyectos'

    def __str__(self):
        return self.id




#Prospecciones########################
class Prospecciones(models.Model):
    n = models.AutoField(primary_key=True)
    tipo_prospeccion = models.CharField(max_length=25, choices=[
        ('sondajes', 'Sondajes'),
        ('calicatas', 'Calicatas'),
        ('geofisica', 'Geofísica'),
    ], null=False)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    id_prospeccion = models.CharField(max_length=25, null=False, unique=True)  # Asegurando unicidad en Prospecciones
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
    inclinacion = models.IntegerField(null=True, blank=True)  # Solo para sondajes
    diametro = models.IntegerField(null=True, blank=True)  # Solo para sondajes
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuario que realiza la operación
    history = HistoricalRecords()  # Agregar el historial de registros

    class Meta:
        db_table = 'prospecciones'

    def __str__(self):
        return self.id_prospeccion



# Muestreo########################
class Muestreo(models.Model):
    n = models.AutoField(primary_key=True)   
    id_embalaje = models.CharField(max_length=255, null=False, blank=False)  # Concatenar "id_prospeccion"_"(profundidad_desde-profundiad_hasta)"_"id_muestra"   
    id_proyecto = models.ForeignKey('Proyectos', on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion', related_name='muestreos_por_id')   
    area = models.CharField(max_length=50, null=False, blank=False)  # Se completa automático    
    fecha_muestreo = models.DateField(null=True, blank=True)
    tipo_embalaje = models.CharField(max_length=25, choices=[
        ('caja_nucleo', 'caja_nucleo'),
        ('bolsa_muestra', 'bolsa_muestra'),
        ('saco_muestra', 'saco_muestra'),
        ('tubo_pvc', 'tubo_pvc'),
        ('tambor', 'tambor'),
    ], null=True, blank=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Mostrar en el HTML solo si "tipo_prospeccion" es = calicata
    peso_unitario = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Mostrar en el HTML solo si "tipo_prospeccion" es = calicata
    peso_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Se calcula automático -> "peso_unitario" * "cantidad"    
    id_muestra = models.CharField(max_length=50, null=False, blank=False)
    profundidad_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    profundidad_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)    
    estrato = models.CharField(max_length=25, choices=[
        ('h1', 'h1'),
        ('h2', 'h2'),
        ('h3', 'h3'),
        ('h4', 'h4'),
        ('h5', 'h5'),
        ('h6', 'h6'),
        ('h7', 'h7'),
        ('h8', 'h8'),
    ], null=True, blank=True)  # Mostrar en el HTML solo si "tipo_prospeccion" es = calicata    
    tipo = models.CharField(max_length=25, choices=[
        ('perturbada', 'perturbada'),
        ('no_perturbada', 'no_perturbada'),
        ('colpa', 'colpa'),
    ], null=True, blank=True)
    fecha_despacho = models.DateField(null=True, blank=True)
    nombre_despachador = models.CharField(max_length=50, null=True, blank=True)
    destino = models.CharField(max_length=50, null=True, blank=True)
    orden_trasporte = models.CharField(max_length=50, null=True, blank=True)    
    observacion = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'muestreo'

    def __str__(self):
        return f"Prospección: {self.id_prospeccion.id_prospeccion}, Muestra: {self.id_muestra}, Embalaje: {self.id_embalaje}"


#Programa########################
class Programa(models.Model):
    n = models.AutoField(primary_key=True)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    objetivo = models.CharField(max_length=255, choices=[
        ('clasificacion completa','clasificacion completa'),
        ('humedad','humedad'),
        ('sales solubles, cloruros y sulfatos','sales solubles, cloruros y sulfatos'),
        ('carbonatos','carbonatos'),
        ('triaxial ciu/cid 15x30 hasta 6kg cm2','triaxial ciu/cid 15x30 hasta 6kg cm2'),
        ('triaxial ciu/cid 15x30 hasta 9kg cm2','triaxial ciu/cid 15x30 hasta 9kg cm2'),
        ('granulometria','granulometria'),
        ('peso unitario','peso unitario'),
        ('difraccion de rayos x','difraccion de rayos x'),
        ('triaxial ciu/cid 5x10 hasta 6kg cm2','triaxial ciu/cid 5x10 hasta 6kg cm2'),
        ('triaxial ciu/cid 5x10 hasta 30kg cm2','triaxial ciu/cid 5x10 hasta 30kg cm2'),
        ('impurezas organicas','impurezas organicas'),
        ('sales solubles totales','sales solubles totales'),
        ('resistencia al desgaste, metodo los angeles','resistencia al desgaste, metodo los angeles'),
        ('densidad in situ','densidad in situ'),
        ('densidad aparente','densidad aparente'),
        ('resistencia a la desintegracion','resistencia a la desintegracion'),
        ('uscs','uscs'),
        ('triaxial ciu/cid 10x20 hasta 6kg cm2','triaxial ciu/cid 10x20 hasta 6kg cm2'),
        ('triaxial ciu/cid 10x20 hasta 12kg cm2','triaxial ciu/cid 10x20 hasta 12kg cm2'),
        ('densidad maxima y minima','densidad maxima y minima'),
        ('permeabilidad pared flexible carga constante (10x20 hasta 6 kg/cm2)','permeabilidad pared flexible carga constante (10x20 hasta 6 kg/cm2)'),
        ('permeabilidad pared flexible carga constante (15x30 hasta 6 kg/cm2)','permeabilidad pared flexible carga constante (15x30 hasta 6 kg/cm2)'),
        ('cbr','cbr'),
        ('slake durability','slake durability'),
        ('proctor modificado','proctor modificado'),
        ('corte directo','corte directo'),
        ('ph','ph'),
        ('determinacion de propiedades fisicas','determinacion de propiedades fisicas'),
        ('resistividad electrica','resistividad electrica'),
        ('compresion simple','compresion simple'),
        ('carga puntual','carga puntual'),
        ('traccion indirecta, metodo brasileno','traccion indirecta, metodo brasileno'),
        ('triaxial con medicion de deformacion axial y transversal','triaxial con medicion de deformacion axial y transversal'),
    ], null=True, blank=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha_ingreso_lab = models.DateField(null=True, blank=True)
    id_ingreso = models.CharField(max_length=50, null=False, blank=False)
    area = models.CharField(max_length=50, null=False, blank=False)
    fecha_envio_programa = models.DateField(null=True, blank=True)
    asignar_muestra = models.CharField(max_length=50, null=True, blank=True)
    fecha_informe =  models.DateField(null=True, blank=True)
    cantidad_recibida = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    n_informe = models.CharField(max_length=50, null=True, blank=True)
    n_ep = models.CharField(max_length=50, null=True, blank=True)


#Humedad########################
class Humedad(models.Model):
    n = models.AutoField(primary_key=True)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    humedad = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    profundidad_promedio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    area = models.CharField(max_length=50, null=True, blank=True)
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuario que realiza la operación


    class Meta:
        db_table = 'humedad'


class Area(models.Model):
    nombre = models.CharField(max_length=255)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuario que realiza la operación

    class Meta:
        db_table = 'area'



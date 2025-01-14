from mailbox import NoSuchMailboxError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
import json
from django.core.exceptions import ValidationError



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
    area = models.CharField(max_length=50, null=False, blank=False)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    coordenada_este = models.CharField(max_length=6, null=True, blank=True)
    coordenada_norte = models.CharField(max_length=7, null=True, blank=True)
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

    class Meta:
        db_table = 'prospecciones'

    def __str__(self):
        return self.id_prospeccion


#Muestreo########################
class Muestreo(models.Model):
    n = models.AutoField(primary_key=True)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, db_column='id_proyecto', to_field='id')
    tipo_prospeccion = models.CharField(max_length=25, null=True, blank=True)
    id_prospeccion = models.ForeignKey(Prospecciones, on_delete=models.CASCADE, db_column='id_prospeccion', to_field='id_prospeccion')
    fecha_muestreo = models.DateField(null=True, blank=True)
    n_muestra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    embalaje = models.CharField(max_length=25, choices=[
        ('caja_nucleo', 'caja_nucleo'),
        ('bolsa_muestra', 'bolsa_muestra'),
        ('saco_muestra', 'saco_muestra'),
        ('tubo_pvc', 'tubo_pvc'),
        ('tambor', 'tambor'),
    ], null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cota_desde = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cota_hasta = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estrato = models.CharField(max_length=25, choices=[
        ('h1', 'h1'),
        ('h2', 'h2'),
        ('h3', 'h3'),
        ('h4', 'h4'),
        ('h5', 'h5'),
        ('h6', 'h6'),
        ('h7', 'h7'),
        ('h8', 'h8'),
    ], null=True, blank=True)
    tipo = models.CharField(max_length=25, choices=[
        ('perturbada', 'perturbada'),
        ('no_perturbada', 'no_perturbada'),
        ('colpa', 'colpa'),
    ], null=True, blank=True)
    area = models.CharField(max_length=50, null=False, blank=False)
    observacion = models.CharField(max_length=255, null=True, blank=True)
    tipo_prospeccion = models.CharField(max_length=25, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'muestreo'

    def __str__(self):
        # Devolver una representación más detallada del muestreo
        return f"Prospección: {self.id_prospeccion.id_prospeccion}, Muestra: {self.n_muestra}, Embalaje: {self.embalaje}"

    # Validación personalizada para evitar duplicados de n_muestra y embalaje en la misma id_prospeccion
    def clean(self):
        # Verificar si ya existe una entrada con el mismo n_muestra y embalaje dentro de la misma id_prospeccion
        if Muestreo.objects.filter(id_prospeccion=self.id_prospeccion, embalaje=self.embalaje, n_muestra=self.n_muestra).exists():
            raise ValidationError('Ya existe una entrada con el mismo n_muestra y embalaje en la misma prospección.')

    # Sobrescritura del método save para llamar a clean antes de guardar la instancia
    def save(self, *args, **kwargs):
        self.clean()  # Llamar a la validación personalizada
        super(Muestreo, self).save(*args, **kwargs)  # Llamar al método save del modelo base




#########GRAFICOS############################################
#Humedad
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



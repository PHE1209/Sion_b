from mailbox import NoSuchMailboxError
from django.db import models
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
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=25, null = False)
    nombre = models.CharField(max_length=25, null = False)
    apellido = models.CharField(max_length=25, null = False)
    email = models.CharField(max_length=50, null = False)
    telefono = models.CharField(max_length=15, null=False)
    class Meta:
        db_table = 'usuarios'


class Proyectos(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    pm = models.CharField(max_length=25, null = False)
    empresa = models.CharField(max_length=25, null = False)
    nombre = models.CharField(max_length=25, null = False)
    fecha_inicio = models.DateField(null=True, blank=True)  # Permitir NULL
    fecha_termino = models.DateField(null=True, blank=True)  # Permitir NULL
    alcance = models.CharField(max_length=255, null = False)
    class Meta:
        db_table = 'proyectos'

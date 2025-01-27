# forms.py
from django import forms
from .models import Proyectos, Prospecciones, Proyectos, Humedad, Muestreo, Programa # Asegúrate de importar tu modelo
from django.forms.widgets import TextInput, DateInput
import re


#formulario de inicio de sesión definido.

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

## CREAR PROYECTOS ###############################################
class ProyectoEditForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['estatus_proyecto', 'id', 'pm', 'empresa', 'nombre', 'fecha_inicio', 'fecha_termino', 'alcance']
        widgets = {
            'estatus_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'pm': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'alcance': forms.Textarea(attrs={'class': 'form-control'}),

            
        }


##En tu archivo forms.py, añade una utilidad para aplicar clases CSS a los campos del formulario. Puedes usar la siguiente función:

def add_class(field, css_class):
    if hasattr(field, 'widget') and isinstance(field.widget, TextInput):
        field.widget.attrs.update({'class': css_class})
    return field

class ProyectoEditForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['estatus_proyecto', 'id', 'pm', 'empresa', 'nombre', 'fecha_inicio', 'fecha_termino', 'alcance']
        widgets = {
            'fecha_inicio': DateInput(attrs={'class': 'form-control'}),
            'fecha_termino': DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProyectoEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields[field_name] = add_class(field, 'form-control')

######################################################################
# PARA PROSPECCIONES
# Agregar prospecciones
class ProspeccionesForm(forms.ModelForm):
    id_proyecto = forms.ModelChoiceField(
        queryset=Proyectos.objects.all(),
        empty_label="Seleccione un proyecto",
        to_field_name="id",
        widget=forms.Select,
    )

    class Meta:
        model = Prospecciones
        fields = [
            'tipo_prospeccion', 'area', 'fecha_inicio', 'fecha_termino', 'id_proyecto', 'id_prospeccion',
            'coordenada_este', 'coordenada_norte', 'elevacion', 'profundidad', 'observacion', 'verificacion_puntos',
            'plataforma', 'inclinacion', 'diametro', 'tapado', 'contratista', 'marca_maquina1', 'modelo_maquina1',
            'ppu1', 'marca_maquina2', 'modelo_maquina2', 'ppu2', 'image'
        ]

    def clean_id_proyecto(self):
        id_proyecto = self.cleaned_data.get('id_proyecto')
        if not Proyectos.objects.filter(id=id_proyecto).exists():
            raise forms.ValidationError("Este proyecto no existe en la base de datos.")
        return id_proyecto

# PARA MUESTREO
# forms.py
from django import forms
from .models import Muestreo

class MuestreoForm(forms.ModelForm):
    class Meta:
        model = Muestreo
        fields = '__all__'

######################################################################

#Agregar humedad
class HumedadForm(forms.ModelForm):
    id_proyecto = forms.ModelChoiceField(queryset=Proyectos.objects.all(), label='ID Proyecto', required=True)
    id_prospeccion = forms.ModelChoiceField(queryset=Prospecciones.objects.all(), label='Prospección', required=True)
    tipo_prospeccion = forms.CharField(max_length=25, label='Tipo Prospección')

    class Meta:
        model = Humedad
        fields = ['id_proyecto', 'id_prospeccion', 'tipo_prospeccion', 'humedad', 'profundidad_promedio', 'area']



#Agregar programa
class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = '__all__'
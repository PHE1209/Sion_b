# forms.py
from django import forms
from .models import Proyectos, Prospecciones, Proyectos, Humedad, Muestreo # Asegúrate de importar tu modelo
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

#PARA PROSPECCIONES
#Agregar prospecciones
class ProspeccionesForm(forms.ModelForm):
    id_proyecto = forms.ModelChoiceField(
        queryset=Proyectos.objects.all(),  # Obtiene todos los proyectos
        empty_label="Seleccione un proyecto",  # Etiqueta predeterminada para un campo vacío
        to_field_name="id",  # Especificamos que el valor a enviar será el 'id', no el 'nombre'
        widget=forms.Select,  # Puedes personalizar el widget si lo deseas
    )

    class Meta:
        model = Prospecciones
        fields = [
            'tipo_prospeccion', 'area', 'fecha_inicio', 'fecha_termino', 'id_proyecto', 'id_prospeccion',
            'coordenada_este', 'coordenada_norte', 'elevacion', 'profundidad', 'observacion', 'verificacion_puntos',
            'plataforma', 'inclinacion', 'diametro', 'tapado', 'contratista', 'marca_maquina1', 'modelo_maquina1',
            'ppu1', 'marca_maquina2', 'modelo_maquina2', 'ppu2', 'image'  # Incluir el campo de imagen
        ]

    
    # Validación personalizada para el campo 'id_proyecto'
    def clean_id_proyecto(self):
        id_proyecto = self.cleaned_data.get('id_proyecto')
        # Validación de existencia del proyecto (si quieres personalizarlo más)
        if not Proyectos.objects.filter(id=id_proyecto).exists():
            raise forms.ValidationError("Este proyecto no existe en la base de datos.")
        return id_proyecto


######################################################################
##MUESTREO
class MuestreoForm(forms.ModelForm):
    class Meta:
        model = Muestreo
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        n_muestra = cleaned_data.get("n_muestra")
        embalaje = cleaned_data.get("embalaje")

        if n_muestra and embalaje and n_muestra == embalaje:
            self.add_error('n_muestra', "El número de muestra y el embalaje no pueden ser los mismos.")
            self.add_error('embalaje', "El número de muestra y el embalaje no pueden ser los mismos.")
        return cleaned_data

######################################################################

#Agregar humedad
class HumedadForm(forms.ModelForm):
    id_proyecto = forms.ModelChoiceField(queryset=Proyectos.objects.all(), label='ID Proyecto', required=True)
    id_prospeccion = forms.ModelChoiceField(queryset=Prospecciones.objects.all(), label='Prospección', required=True)
    tipo_prospeccion = forms.CharField(max_length=25, label='Tipo Prospección')

    class Meta:
        model = Humedad
        fields = ['id_proyecto', 'id_prospeccion', 'tipo_prospeccion', 'humedad', 'profundidad_promedio', 'area']



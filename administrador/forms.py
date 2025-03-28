# forms.py
from django import forms
from .models import Proyectos, Prospecciones, Proyectos, Humedad, Muestreo, Programa, Granulometria, Nomina # Asegúrate de importar tu modelo
from django.forms.widgets import TextInput, DateInput
import re
from django import forms
from .models import Muestreo
from django import forms
from .models import Programa, Proyectos, Prospecciones
from django import forms
from .models import Muestreo

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


#Muestreo
class MuestreoForm(forms.ModelForm):
    class Meta:
        model = Muestreo
        fields = [
            'id_proyecto', 'id_prospeccion', 'area', 'fecha_muestreo', 'id_muestra',
            'tipo_embalaje', 'cantidad', 'peso_unitario', 'peso_total',
            'profundidad_desde', 'profundidad_hasta', 'estrato', 'tipo',
            'nombre_despachador', 'fecha_despacho', 'destino', 'orden_transporte',  # Corregido
            'observacion'
        ]
        widgets = {
            'fecha_muestreo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_despacho': forms.DateInput(attrs={'type': 'date'}),
            'observacion': forms.Textarea(attrs={'rows': 3}),
        }

#Agregar humedad
class HumedadForm(forms.ModelForm):
    class Meta:
        model = Humedad
        fields = [
            'id_proyecto', 'id_prospeccion', 'humedad', 'profundidad_promedio', 
            'area', 'tipo_prospeccion'
        ]               
        
#Agregar programa
class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = [
            'id_proyecto', 'tipo_prospeccion', 'id_prospeccion', 'objetivo', 'cantidad',
            'fecha_ingreso_lab', 'id_ingreso', 'area', 'fecha_envio_programa', 'asignar_muestra',
            'fecha_informe', 'cantidad_recibida', 'n_informe', 'n_ep'
        ]
        widgets = {
            'fecha_ingreso_lab': forms.DateInput(attrs={'type': 'date'}),
            'fecha_envio_programa': forms.DateInput(attrs={'type': 'date'}),
            'fecha_informe': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Personalizar los campos de claves foráneas
        self.fields['id_proyecto'].queryset = Proyectos.objects.all()
        self.fields['id_prospeccion'].queryset = Prospecciones.objects.all()
        
##Granulometria
class GranulometriaForm(forms.ModelForm):
    class Meta:
        model = Granulometria
        fields = [
            'id_proyecto', 'id_prospeccion', 'n_0075', 'n_0110', 'n_0250', 
            'n_0420', 'n_0840', 'n_2000', 'n_4760', 'n_9520', 'n_19000', 
            'n_25400', 'n_38100', 'n_50800', 'n_63500', 'n_75000', 'area', 'tipo_prospeccion'
        ]      


class NominaForm(forms.ModelForm):
    class Meta:
        model = Nomina
        fields = '__all__'
        exclude = ['user', 'horas_por_dia_lista', 'total_horas', 'horas_semanales', 'horas_mensuales', 'history']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'primer_dia': forms.DateInput(attrs={'type': 'date'}),
            'ultimo_dia': forms.DateInput(attrs={'type': 'date'}),
        }
        

from django import forms
from .models import uscs

class UscsForm(forms.ModelForm):
    class Meta:
        model = uscs
        fields = ['id_proyecto', 'tipo_prospeccion', 'id_prospeccion', 'id_muestra', 'uscs', 'area', 'profundidad_desde', 'profundidad_hasta']
        widgets = {
            'area': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_desde': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_hasta': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
from django import forms
from .models import gravedad_especifica

class GravedadEspecificaForm(forms.ModelForm):
    class Meta:
        model = gravedad_especifica
        fields = ['id_proyecto', 'tipo_prospeccion', 'id_prospeccion', 'id_muestra', 'gravedad_especifica', 'area', 'profundidad_desde', 'profundidad_hasta']
        widgets = {
            'area': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_desde': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_hasta': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
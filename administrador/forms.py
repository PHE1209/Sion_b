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
from django import forms
from .models import Prospecciones, ProspeccionImage

class ProspeccionesForm(forms.ModelForm):
    imagenes = forms.ModelMultipleChoiceField(
        queryset=ProspeccionImage.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Prospecciones
        fields = [
            'id_proyecto', 'tipo_prospeccion', 'tipo_sondaje', 'metodologia_sondaje',
            'metodologia_geofisica', 'id_prospeccion', 'area', 'fecha_inicio_perforacion',
            'fecha_termino_perforacion', 'coordenada_este', 'coordenada_norte', 'elevacion',
            'profundidad', 'inclinacion', 'diametro_sondaje', 'habilitacion', 'monolito',
            'tapado', 'contratista', 'marca_maquina1', 'modelo_maquina1', 'ppu1',
            'marca_maquina2', 'modelo_maquina2', 'ppu2', 'observacion', 'imagenes'
        ]
        widgets = {
            'fecha_inicio_perforacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino_perforacion': forms.DateInput(attrs={'type': 'date'}),
            'coordenada_este': forms.TextInput(attrs={
                'pattern': r'\d{6}\.\d{1,3}',
                'title': 'Formato: 123456.789 (6 enteros, 1-3 decimales)',
                'placeholder': 'Ej: 570168.862'
            }),
            'coordenada_norte': forms.TextInput(attrs={
                'pattern': r'\d{7}\.\d{1,3}',
                'title': 'Formato: 1234567.789 (7 enteros, 1-3 decimales)',
                'placeholder': 'Ej: 5650300.787'
            }),
        }

class ProspeccionImageForm(forms.ModelForm):
    class Meta:
        model = ProspeccionImage
        fields = ['image']

class ProspeccionImageForm(forms.ModelForm):
    class Meta:
        model = ProspeccionImage
        fields = ['image']
        
#Muestreo
# forms.py
from django import forms
from .models import Muestreo, MuestreoImage

class MuestreoForm(forms.ModelForm):
    imagenes = forms.ModelMultipleChoiceField(
        queryset=MuestreoImage.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Muestreo
        fields = [
            'id_proyecto', 'tipo_prospeccion', 'id_prospeccion', 'area', 'fecha_muestreo',
            'objetivo', 'id_bulto', 'tipo_bulto', 'id_embalaje_muestra', 'tipo_embalaje_muestra',
            'id_muestra', 'cantidad', 'peso_unitario', 'peso_total', 'profundidad_desde',
            'profundidad_hasta', 'profundidad_promedio', 'espesor_estrato', 'estrato',
            'tipo', 'fecha_despacho', 'nombre_despachador', 'destino', 'orden_transporte',
            'observacion', 'id_laboratorio', 'imagenes'
        ]
        widgets = {
            'fecha_muestreo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_despacho': forms.DateInput(attrs={'type': 'date'}),
            'cantidad': forms.NumberInput(attrs={'step': '0.01'}),
            'peso_unitario': forms.NumberInput(attrs={'step': '0.01'}),
            'peso_total': forms.NumberInput(attrs={'step': '0.01'}),
            'profundidad_desde': forms.NumberInput(attrs={'step': '0.01'}),
            'profundidad_hasta': forms.NumberInput(attrs={'step': '0.01'}),
            'profundidad_promedio': forms.NumberInput(attrs={'step': '0.01'}),
            'espesor_estrato': forms.NumberInput(attrs={'step': '0.01'}),
            'observacion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['imagenes'].queryset = self.instance.imagenes.all()
        else:
            self.fields['imagenes'].queryset = MuestreoImage.objects.none()
            
from django import forms
from .models import Humedad

class HumedadForm(forms.ModelForm):
    class Meta:
        model = Humedad
        fields = ['id_proyecto', 'tipo_prospeccion', 'id_prospeccion', 'id_muestra', 'humedad', 'area', 'profundidad_desde', 'profundidad_hasta']
        widgets = {
            'area': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_desde': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_hasta': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

          
        
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
        fields = '__all__'


        
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
        

from django import forms
from administrador.models import Limites_atterberg

class LimitesAtterbergForm(forms.ModelForm):
    class Meta:
        model = Limites_atterberg
        fields = [
            'id_proyecto', 'tipo_prospeccion', 'id_prospeccion', 'id_muestra',
            'limite_liquido', 'limite_plastico', 'indice_plasticidad', 'metodo',
            'acanalado', 'area', 'profundidad_desde', 'profundidad_hasta'
        ]
        widgets = {
            'area': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_desde': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_hasta': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        
        
# forms.py
from django import forms
from .models import Granulometria

class GranulometriaForm(forms.ModelForm):
    class Meta:
        model = Granulometria
        fields = [
            'id_proyecto', 'tipo_prospeccion', 'id_prospeccion', 'id_muestra',
            'profundidad_desde', 'profundidad_hasta', 'area',
            'n_0075', 'n_0110', 'n_0250', 'n_0420', 'n_0840', 'n_2000',
            'n_4760', 'n_9520', 'n_19000', 'n_25400', 'n_38100', 'n_50800',
            'n_63500', 'n_75000'
        ]
        widgets = {
            'area': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_desde': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_hasta': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        
from django import forms
from administrador.models import Cbr

class CbrForm(forms.ModelForm):
    class Meta:
        model = Cbr
        fields = [
            'id_proyecto', 'tipo_prospeccion', 'id_prospeccion', 'id_muestra',
            'densidad_seca_ai', 'densidad_seca_di', 'humedad_ai', 'humedad_di',
            'cbr_01', 'cbr_02', 'observacion', 'area', 'profundidad_desde', 'profundidad_hasta'
        ]
        widgets = {
            'area': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_desde': forms.TextInput(attrs={'readonly': 'readonly'}),
            'profundidad_hasta': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
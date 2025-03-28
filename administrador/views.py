from datetime import date, datetime, timedelta
from decimal import Decimal
import base64
import csv
import io
import json
import logging
import os
from io import BytesIO

# Bibliotecas para gráficos y datos
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, LogLocator, MaxNLocator

# Django - Autenticación y Decoradores
from django.apps import apps
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

# Django - Funcionalidades adicionales
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import (
    CharField, DateField, DateTimeField, DecimalField, FloatField,
    ForeignKey, Q, Sum, TextField, F
)
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

# ReportLab
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

# OpenPyXL
from openpyxl import Workbook

# Formularios y Modelos específicos del proyecto
from .forms import (
    GranulometriaForm, HumedadForm, LoginForm, MuestreoForm, NominaForm,
    ProgramaForm, ProyectoEditForm, ProspeccionesForm, GravedadEspecificaForm, UscsForm
)
from .models import (
    Area, Granulometria, Humedad, JornadaTeorica, Muestreo, Nomina,
    Programa, Prospecciones, Proyectos, Roster, gravedad_especifica, uscs
)


# Create your views here.
TEMPLATE_DIR = (
    'os.path.join(BASE_DIR, "templates),'
)

#### INICIO DE SESION  #############################################################################

@login_required
def index_view(request):
    return render(request, 'index.html')

# Inicio de sesión
def home_view(request):
    return render(request, 'home.html')

# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Autenticación usando el correo electrónico
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')  # Redirecciona a la vista index después de iniciar sesión
                else:
                    form.add_error(None, 'Email o contraseña incorrectos.')
            else:
                form.add_error(None, 'Email no registrado.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# Vista protegida usando decorador
@login_required
def mi_vista_protegida(request):
    return render(request, 'index_master.html')

# Vista protegida usando LoginRequiredMixin
class MiVistaProtegida(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

# Vista index
@login_required
def index_view(request):
    return render(request, 'index.html')






#### PROYECTO ##############################################

# Agregar proyecto
@login_required
def agregar_proyectos(request):
    if request.method == 'POST':
        form = ProyectoEditForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.user = request.user
            proyecto.save()
            return redirect('listar_proyectos')
    else:
        form = ProyectoEditForm()
    return render(request, 'proyectos/agregar_proyectos.html', {'form': form})

# Listar proyecto
@login_required
def listar_proyectos(request):
    proyectos = Proyectos.objects.all().order_by('id')
    query = request.GET.get('q', '')
    if query:
        Proyectos_model = apps.get_model('administrador', 'Proyectos')
        fields = [field.name for field in Proyectos_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField))]
        query_filter = Q()
        for field in fields:
            if isinstance(Proyectos_model._meta.get_field(field), (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        proyectos = proyectos.filter(query_filter)

    paginator = Paginator(proyectos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'proyectos/proyectos_table.html', {'page_obj': page_obj})
    return render(request, 'proyectos/listar_proyectos.html', {'page_obj': page_obj, 'query': query})

# Ver proyecto
@login_required
def ver_proyectos(request, id):
    proyecto = get_object_or_404(Proyectos, id=id)
    return render(request, 'proyectos/ver_proyectos.html', {'proyecto': proyecto})

# Eliminar proyecto
@login_required
def eliminar_proyectos(request, id):
    proyecto = get_object_or_404(Proyectos, id=id)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('listar_proyectos')
    return render(request, 'proyectos/eliminar_proyectos.html', {'proyecto': proyecto})

# Editar proyecto
@login_required
def editar_proyectos(request, id):
    proyecto = get_object_or_404(Proyectos, id=id)
    if request.method == 'POST':
        proyecto.pm = request.POST.get('pm')
        proyecto.empresa = request.POST.get('empresa')
        proyecto.nombre = request.POST.get('nombre')
        proyecto.alcance = request.POST.get('alcance')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_termino')
        if fecha_inicio:
            proyecto.fecha_inicio = pd.to_datetime(fecha_inicio, format='%Y-%m-%d').date()
        if fecha_termino:
            proyecto.fecha_termino = pd.to_datetime(fecha_termino, format='%Y-%m-%d').date()
        proyecto.save()
        return redirect('listar_proyectos')
    return render(request, 'proyectos/editar_proyectos.html', {'proyecto': proyecto})

# Exportar a Excel (adaptado de granulometría)
@login_required
def export_to_excel_proyectos(request):
    query = request.GET.get('q', '')
    headers_str = request.GET.get('headers', '')
    headers = headers_str.split(',') if headers_str else [
        'ID', 'Estatus Proyecto', 'PM', 'Empresa', 'Nombre', 'Fecha Inicio', 'Fecha Término', 'Alcance', 'Usuario'
    ]

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="proyectos_filtrados.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Proyectos Filtrados"
    ws.append(headers)

    proyectos = Proyectos.objects.all().order_by('id')
    if query:
        Proyectos_model = apps.get_model('administrador', 'Proyectos')
        fields = [field.name for field in Proyectos_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField))]
        query_filter = Q()
        for field in fields:
            if isinstance(Proyectos_model._meta.get_field(field), (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        proyectos = proyectos.filter(query_filter)

    for proyecto in proyectos:
        row = []
        for header in headers:
            if header == 'ID':
                value = str(proyecto.id)
            elif header == 'Estatus Proyecto':
                value = proyecto.estatus_proyecto or 'N/A'
            elif header == 'PM':
                value = proyecto.pm or 'N/A'
            elif header == 'Empresa':
                value = proyecto.empresa or 'N/A'
            elif header == 'Nombre':
                value = proyecto.nombre or 'N/A'
            elif header == 'Fecha Inicio':
                value = proyecto.fecha_inicio.strftime('%d/%m/%Y') if proyecto.fecha_inicio else 'N/A'
            elif header == 'Fecha Término':
                value = proyecto.fecha_termino.strftime('%d/%m/%Y') if proyecto.fecha_termino else 'N/A'
            elif header == 'Alcance':
                value = proyecto.alcance or 'N/A'
            elif header == 'Usuario':
                value = proyecto.user.username if proyecto.user else 'Sin usuario'
            else:
                value = '-'
            row.append(value)
        ws.append(row)

    wb.save(response)
    return response

# Exportar a PDF
@login_required
def export_to_pdf_proyectos(request):
    query = request.GET.get('q', '')
    headers_str = request.GET.get('headers', '')
    headers = headers_str.split(',') if headers_str else [
        'ID', 'Estatus Proyecto', 'PM', 'Empresa', 'Nombre', 'Fecha Inicio', 'Fecha Término', 'Alcance', 'Usuario'
    ]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="proyectos_filtrados.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Reporte de Proyectos Filtrados")
    p.drawString(100, 730, " | ".join(headers))

    proyectos = Proyectos.objects.all().order_by('id')
    if query:
        Proyectos_model = apps.get_model('administrador', 'Proyectos')
        fields = [field.name for field in Proyectos_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField))]
        query_filter = Q()
        for field in fields:
            if isinstance(Proyectos_model._meta.get_field(field), (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        proyectos = proyectos.filter(query_filter)

    y = 710
    for proyecto in proyectos:
        row = []
        for header in headers:
            if header == 'ID':
                value = str(proyecto.id)
            elif header == 'Estatus Proyecto':
                value = proyecto.estatus_proyecto or 'N/A'
            elif header == 'PM':
                value = proyecto.pm or 'N/A'
            elif header == 'Empresa':
                value = proyecto.empresa or 'N/A'
            elif header == 'Nombre':
                value = proyecto.nombre or 'N/A'
            elif header == 'Fecha Inicio':
                value = proyecto.fecha_inicio.strftime('%d/%m/%Y') if proyecto.fecha_inicio else 'N/A'
            elif header == 'Fecha Término':
                value = proyecto.fecha_termino.strftime('%d/%m/%Y') if proyecto.fecha_termino else 'N/A'
            elif header == 'Alcance':
                value = proyecto.alcance or 'N/A'
            elif header == 'Usuario':
                value = proyecto.user.username if proyecto.user else 'Sin usuario'
            else:
                value = '-'
            row.append(value)
        text = " | ".join(row)
        p.drawString(100, y, text[:500])  # Limitar longitud para evitar desbordamiento
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    return response

#### PROSPECCIONES ##############################################

# Agregar prospecciones
@login_required
def agregar_prospecciones(request):
    form = ProspeccionesForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            prospeccion = form.save(commit=False)
            prospeccion.user = request.user
            prospeccion.save()
            image = request.FILES.get('image')
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                uploaded_file_url = fs.url(filename)
                print(f'Archivo guardado en: {uploaded_file_url}')
            else:
                print('No se recibió imagen.')
            return redirect('listar_prospecciones')
        else:
            print('Formulario no es válido')
            print(form.errors)
    return render(request, 'terreno/prospecciones/agregar_prospecciones.html', {'form': form})

# Listar prospecciones
def listar_prospecciones(request):
    prospecciones = Prospecciones.objects.all().order_by('id_prospeccion')  # Cambiar n por id_prospeccion
    query = request.GET.get('q', '')
    if query:
        Prospecciones_model = apps.get_model('administrador', 'Prospecciones')
        fields = [field.name for field in Prospecciones_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        query_filter = Q()
        for field in fields:
            if isinstance(Prospecciones_model._meta.get_field(field), (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            elif isinstance(Prospecciones_model._meta.get_field(field), ForeignKey):
                related_model = Prospecciones_model._meta.get_field(field).related_model
                related_fields = [f"{field}__{related_field.name}" for related_field in related_model._meta.get_fields() if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    query_filter |= Q(**{f"{related_field}__icontains": query})
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        prospecciones = prospecciones.filter(query_filter)

    paginator = Paginator(prospecciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'terreno/prospecciones/prospecciones_table.html', {'page_obj': page_obj})
    return render(request, 'terreno/prospecciones/listar_prospecciones.html', {'page_obj': page_obj, 'query': query})

# Exportar a excel
def export_to_excel_prospecciones(request):
    prospecciones = Prospecciones.objects.all().values()
    df = pd.DataFrame(prospecciones)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=prospecciones.xlsx'
    df.to_excel(response, index=False)
    return response

def export_to_pdf_prospecciones(request):
    pass

# Ver prospecciones
def ver_prospecciones(request, id_prospeccion):  # Cambiar prospeccion_id por id_prospeccion
    prospeccion = get_object_or_404(Prospecciones, id_prospeccion=id_prospeccion)  # Cambiar n por id_prospeccion
    return render(request, 'ver_prospecciones.html', {'prospeccion': prospeccion})

# Editar prospeccion
@login_required
def editar_prospecciones(request, id_prospeccion):  # Cambiar n por id_prospeccion
    prospeccion = get_object_or_404(Prospecciones, id=id_prospeccion)  # Cambiar pk por id_prospeccion
    proyectos = Proyectos.objects.all()
    if request.method == 'POST':
        form = ProspeccionesForm(request.POST, request.FILES, instance=prospeccion)
        if form.is_valid():
            form.save()
            return redirect('listar_prospecciones')
    else:
        form = ProspeccionesForm(instance=prospeccion)
    return render(request, 'terreno/prospecciones/editar_prospecciones.html', {
        'form': form,
        'prospeccion': prospeccion,
        'proyectos': proyectos,
    })

# Eliminar prospeccion
def eliminar_prospecciones(request, id_prospeccion):  # Cambiar n por id_prospeccion
    prospeccion = get_object_or_404(Prospecciones, id_prospeccion=id_prospeccion)  # Cambiar pk por id_prospeccion
    prospeccion.delete()
    return redirect('listar_prospecciones')


#### Funciones comunes para modulos de laboratorio ##############################################

# Funciones transversales (aplican a ambos modelos o usan Prospecciones)
# Estas funciones son comunes y no dependen específicamente de Humedad o Granulometria

logger = logging.getLogger(__name__)

# Funciones comunes
def obtener_proyectos_prospecciones(request, as_json=False):
    proyectos = Granulometria.objects.values('id_proyecto').distinct()
    proyectos_list = [proj['id_proyecto'] for proj in proyectos if proj['id_proyecto'] is not None]
    proyectos_dict = {proj: proj for proj in proyectos_list}
    if as_json:
        return JsonResponse(proyectos_dict, safe=False)
    return proyectos_list

# Funciones de prospección
def obtener_tipos_prospeccion(request):
    id_proyecto = request.GET.get('id_proyecto')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto).values('tipo_prospeccion').distinct()
    tipos_prospeccion = {pros['tipo_prospeccion']: pros['tipo_prospeccion'] for pros in prospecciones}
    return JsonResponse(tipos_prospeccion)

def obtener_id_prospecciones(request):
    id_proyecto = request.GET.get('id_proyecto')
    tipo_prospeccion = request.GET.get('tipo_prospeccion')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto, tipo_prospeccion=tipo_prospeccion).values('id_prospeccion')
    id_prospecciones = {pros['id_prospeccion']: pros['id_prospeccion'] for pros in prospecciones}
    return JsonResponse(id_prospecciones)

def get_area(request):
    prospeccion_id = request.GET.get('prospeccion_id')
    try:
        prospeccion = Prospecciones.objects.get(id_prospeccion=prospeccion_id)
        area = prospeccion.area
    except Prospecciones.DoesNotExist:
        area = ''
    return JsonResponse({'area': area})



####### GRAVEDAD ESPECIFICA #######################
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Proyectos, Muestreo, gravedad_especifica

logger = logging.getLogger(__name__)

@login_required
def agregar_gravedad_especifica(request):
    proyectos_con_muestreo = Proyectos.objects.filter(muestreo__isnull=False).distinct()
    tipo_prospeccion_choices = []
    prospecciones = []
    muestras = []
    area = ""

    if request.method == 'POST':
        logger.info(f"Datos POST recibidos: {request.POST}")
        proyecto_id = request.POST.get('id_proyecto')
        tipo_prospeccion = request.POST.get('tipo_prospeccion')
        id_prospecciones = request.POST.getlist('id_prospeccion[]')
        id_muestras = request.POST.getlist('id_muestra[]')
        gravedades = request.POST.getlist('gravedad_especifica[]')
        errors = []

        if not proyecto_id:
            errors.append("Debe seleccionar un proyecto.")
            return render(request, 'laboratorio/ensayos/gravedad_especifica/agregar_gravedad_especifica.html', {
                'proyectos': proyectos_con_muestreo,
                'errors': errors
            })

        muestreos = Muestreo.objects.filter(id_proyecto_id=proyecto_id)
        if not muestreos.exists():
            errors.append("No hay muestreos asociados a este proyecto.")
            return render(request, 'laboratorio/ensayos/gravedad_especifica/agregar_gravedad_especifica.html', {
                'proyectos': proyectos_con_muestreo,
                'errors': errors
            })

        if tipo_prospeccion:
            muestreos = muestreos.filter(tipo_prospeccion=tipo_prospeccion)
            if not muestreos.exists():
                errors.append("No hay muestreos con este tipo de prospección.")

        if id_prospecciones and id_prospecciones[0]:
            muestreos = muestreos.filter(id_prospeccion__id_prospeccion__in=id_prospecciones)
            if not muestreos.exists():
                errors.append("No hay muestreos con las prospecciones seleccionadas.")

        if id_muestras and id_muestras[0]:
            muestreos = muestreos.filter(id_muestra__in=id_muestras)
            if not muestreos.exists():
                errors.append("No hay muestreos con las muestras seleccionadas.")

        if not (len(id_prospecciones) == len(id_muestras) == len(gravedades)):
            errors.append("El número de prospecciones, muestras y gravedades específicas no coincide.")
            logger.error(f"Longitudes inconsistentes: prospecciones={len(id_prospecciones)}, muestras={len(id_muestras)}, gravedades={len(gravedades)}")
        else:
            for id_pros, id_muestra, gravedad in zip(id_prospecciones, id_muestras, gravedades):
                if not id_pros or not id_muestra or not gravedad:
                    errors.append(f"Falta ID de prospección ({id_pros}), ID de muestra ({id_muestra}) o gravedad específica ({gravedad}).")
                    continue
                
                try:
                    muestreo = muestreos.get(id_prospeccion__id_prospeccion=id_pros, id_muestra=id_muestra)
                    gravedad_obj = gravedad_especifica(
                        id_proyecto=muestreo.id_proyecto,
                        tipo_prospeccion=muestreo.tipo_prospeccion,
                        id_prospeccion=muestreo.id_prospeccion,
                        id_muestra=muestreo.id_muestra,
                        profundidad_desde=muestreo.profundidad_desde,
                        profundidad_hasta=muestreo.profundidad_hasta,
                        profundidad_promedio=(
                            (float(muestreo.profundidad_desde) + float(muestreo.profundidad_hasta)) / 2 
                            if muestreo.profundidad_desde and muestreo.profundidad_hasta else 0
                        ),
                        gravedad_especifica=float(gravedad),
                        area=muestreo.area,
                        user=request.user
                    )
                    gravedad_obj.save()
                    logger.info(f"Gravedad específica guardada: ID={gravedad_obj.id}, Muestra={id_muestra}, Gravedad={gravedad}")
                except Muestreo.DoesNotExist:
                    errors.append(f"Muestra {id_muestra} con prospección {id_pros} no encontrada.")
                except ValueError as e:
                    errors.append(f"Valor inválido para gravedad específica {gravedad}: {e}")
                except Exception as e:
                    errors.append(f"Error al guardar muestra {id_muestra}: {e}")

        if errors:
            tipo_prospeccion_choices = Muestreo.objects.filter(id_proyecto_id=proyecto_id).values_list('tipo_prospeccion', flat=True).distinct()
            prospecciones = Muestreo.objects.filter(id_proyecto_id=proyecto_id).values_list('id_prospeccion__id_prospeccion', flat=True).distinct()
            muestras = Muestreo.objects.filter(id_proyecto_id=proyecto_id).values_list('id_muestra', flat=True).distinct()
            area = muestreos.first().area if muestreos.exists() else ""
            return render(request, 'laboratorio/ensayos/gravedad_especifica/agregar_gravedad_especifica.html', {
                'proyectos': proyectos_con_muestreo,
                'tipo_prospeccion_choices': tipo_prospeccion_choices,
                'prospecciones': prospecciones,
                'muestras': muestras,
                'area': area,
                'errors': errors
            })

        return redirect('listar_gravedad_especifica')

    # Lógica para GET y AJAX
    proyecto_id = request.GET.get('id_proyecto')
    tipo_prospeccion = request.GET.get('tipo_prospeccion')
    id_prospeccion = request.GET.get('id_prospeccion')
    id_muestra = request.GET.get('id_muestra')

    muestreos = Muestreo.objects.all()
    if proyecto_id:
        muestreos = muestreos.filter(id_proyecto_id=proyecto_id)
        tipo_prospeccion_choices = muestreos.values_list('tipo_prospeccion', flat=True).distinct()
        prospecciones = muestreos.values_list('id_prospeccion__id_prospeccion', flat=True).distinct()
        muestras = muestreos.values_list('id_muestra', flat=True).distinct()
        area = muestreos.first().area if muestreos.exists() else ""

    if tipo_prospeccion:
        muestreos = muestreos.filter(tipo_prospeccion=tipo_prospeccion)
        prospecciones = muestreos.values_list('id_prospeccion__id_prospeccion', flat=True).distinct()
        muestras = muestreos.values_list('id_muestra', flat=True).distinct()

    if id_prospeccion:
        muestreos = muestreos.filter(id_prospeccion__id_prospeccion=id_prospeccion)
        muestras = muestreos.values_list('id_muestra', flat=True).distinct()

    # Reemplazo de request.is_ajax() por verificación manual
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        data = {
            'tipo_prospeccion_choices': list(tipo_prospeccion_choices),
            'prospecciones': list(prospecciones),
            'muestras': list(muestras),
            'area': area
        }
        if id_muestra:
            muestreo = muestreos.filter(id_muestra=id_muestra).first()
            if muestreo:
                data['profundidad_desde'] = str(muestreo.profundidad_desde) if muestreo.profundidad_desde else ''
                data['profundidad_hasta'] = str(muestreo.profundidad_hasta) if muestreo.profundidad_hasta else ''
        return JsonResponse(data)

    return render(request, 'laboratorio/ensayos/gravedad_especifica/agregar_gravedad_especifica.html', {
        'proyectos': proyectos_con_muestreo,
        'tipo_prospeccion_choices': tipo_prospeccion_choices,
        'prospecciones': prospecciones,
        'muestras': muestras,
        'area': area
    })


@login_required
def listar_gravedad_especifica(request):
    gravedad_list = gravedad_especifica.objects.all().order_by('id')  # Ordenar por 'id'
    query = request.GET.get('q', '')

    if query:
        gravedad_model = apps.get_model('administrador', 'gravedad_especifica') 
        # Incluir campos de texto y numéricos
        campos = [field.name for field in gravedad_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField, DecimalField, FloatField, ForeignKey))]
        query_filter = Q()

        # Intentar convertir el query a float para búsquedas numéricas
        try:
            query_numeric = float(query)
            numeric_search = True
        except ValueError:
            numeric_search = False

        for field in campos:
            field_instance = gravedad_model._meta.get_field(field)
            if isinstance(field_instance, (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            elif isinstance(field_instance, ForeignKey):
                related_model = field_instance.related_model
                related_fields = [f"{field}__{related_field.name}" for related_field in related_model._meta.get_fields() if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    query_filter |= Q(**{f"{related_field}__icontains": query})
            elif isinstance(field_instance, (DecimalField, FloatField)) and numeric_search:
                # Para campos numéricos, usar coincidencia exacta
                query_filter |= Q(**{f"{field}": query_numeric})
            else:
                # Para campos de texto
                query_filter |= Q(**{f"{field}__icontains": query})

        gravedad_list = gravedad_list.filter(query_filter)

    paginator = Paginator(gravedad_list, 1000)  # 1000 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Si es una solicitud AJAX (opcional)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'laboratorio/ensayos/gravedad_especifica/gravedad_table.html', {'page_obj': page_obj})

    return render(request, 'laboratorio/ensayos/gravedad_especifica/listar_gravedad_especifica.html', {
        'page_obj': page_obj,
        'query': query
    })


@login_required
def editar_gravedad_especifica(request, id):
    gravedad_obj = get_object_or_404(gravedad_especifica, id=id)
    muestreo = Muestreo.objects.filter(id_muestra=gravedad_obj.id_muestra).first()
    proyectos = Proyectos.objects.filter(muestreo__isnull=False).distinct()

    if request.method == 'POST':
        form = GravedadEspecificaForm(request.POST, instance=gravedad_obj)
        if form.is_valid():
            try:
                gravedad_obj = form.save()
                logger.info(f"Gravedad específica editada: ID {gravedad_obj.id}")
                return redirect('listar_gravedad_especifica')
            except Exception as e:
                logger.error(f"Error al editar: {e}")
                form.add_error(None, f"Error al editar: {e}")
    else:
        form = GravedadEspecificaForm(instance=gravedad_obj)
    
    return render(request, 'laboratorio/ensayos/gravedad_especifica/editar_gravedad_especifica.html', {
        'form': form,
        'gravedad_especifica_obj': gravedad_obj,
        'proyectos': proyectos
    })

@login_required
def ver_gravedad_especifica(request, id):
    gravedad_obj = get_object_or_404(gravedad_especifica, id=id)
    return render(request, 'laboratorio/ensayos/gravedad_especifica/ver_gravedad_especifica.html', {
        'gravedad_especifica': gravedad_obj
    })

@login_required
def eliminar_gravedad_especifica(request, id):
    gravedad_obj = get_object_or_404(gravedad_especifica, id=id)
    if request.method == 'POST':
        gravedad_obj.delete()
        return redirect('listar_gravedad_especifica')
    return render(request, 'laboratorio/ensayos/gravedad_especifica/eliminar_gravedad_especifica.html', {
        'gravedad_especifica': gravedad_obj
    })

#Exportar excel
logger = logging.getLogger(__name__)

@login_required
def export_to_excel_gravedad_especifica(request):
    query = request.GET.get('q', '').strip()
    headers = ['ID', 'ID Proyecto', 'ID Prospección', 'Tipo Prospección', 'ID Muestra', 
               'Profundidad Desde', 'Profundidad Hasta', 'Profundidad Promedio', 
               'Gravedad Específica', 'Área', 'Usuario']

    # Crear el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="gravedad_especifica_filtrado.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Gravedad Específica"
    ws.append(headers)

    # Obtener queryset base
    try:
        gravedad_list = gravedad_especifica.objects.select_related(
            'id_proyecto', 'id_prospeccion', 'user'
        ).prefetch_related('id_muestra__muestreo_set').all()

        logger.debug(f"Registros iniciales: {gravedad_list.count()}, query: '{query}'")

        # Aplicar filtros si hay query
        if query:
            filtros = Q()
            
            # Campos numéricos
            try:
                query_numeric = float(query)
                filtros |= (
                    Q(profundidad_desde=query_numeric) |
                    Q(profundidad_hasta=query_numeric) |
                    Q(profundidad_promedio=query_numeric) |
                    Q(gravedad_especifica=query_numeric)
                )
            except ValueError:
                pass

            # Campos de texto y relaciones
            filtros |= (
                Q(id__icontains=query) |
                Q(id_proyecto__id__icontains=query) |
                Q(id_prospeccion__id_prospeccion__icontains=query) |
                Q(tipo_prospeccion__icontains=query) |
                Q(id_muestra__icontains=query) |
                Q(user__username__icontains=query)
            )

            gravedad_list = gravedad_list.filter(filtros)
        
        logger.debug(f"Registros después del filtro: {gravedad_list.count()}")

        # Construir las filas
        for gravedad in gravedad_list:
            try:
                muestreo = Muestreo.objects.filter(id_muestra=gravedad.id_muestra).first()
                
                row = [
                    str(gravedad.id) if gravedad.id is not None else '',
                    str(gravedad.id_proyecto.id) if gravedad.id_proyecto else '',
                    str(gravedad.id_prospeccion.id_prospeccion) if gravedad.id_prospeccion else '',
                    str(gravedad.tipo_prospeccion or ''),
                    str(gravedad.id_muestra or ''),
                    str(gravedad.profundidad_desde) if gravedad.profundidad_desde is not None else '',
                    str(gravedad.profundidad_hasta) if gravedad.profundidad_hasta is not None else '',
                    str(gravedad.profundidad_promedio) if gravedad.profundidad_promedio is not None else '',
                    str(gravedad.gravedad_especifica) if gravedad.gravedad_especifica is not None else '',
                    str(muestreo.area) if muestreo and hasattr(muestreo, 'area') else '',
                    str(gravedad.user.username) if gravedad.user else 'Sin usuario'
                ]
                ws.append(row)
            except Exception as e:
                logger.error(f"Error al procesar registro {gravedad.id}: {str(e)}")
                continue

        wb.save(response)
        return response

    except Exception as e:
        logger.error(f"Error en export_to_excel_gravedad_especifica: {str(e)}")
        ws.append(["Error al generar el reporte", str(e)])
        wb.save(response)
        return response
    
    
#Exportar PDF
logger = logging.getLogger(__name__)

@login_required
def export_to_pdf_gravedad_especifica(request):
    query = request.GET.get('q', '').strip()
    
    # Configurar respuesta HTTP para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="gravedad_especifica_filtrado.pdf"'

    # Configurar documento PDF (carta horizontal)
    doc = SimpleDocTemplate(response, pagesize=landscape(letter), 
                          rightMargin=30, leftMargin=30, 
                          topMargin=30, bottomMargin=30)
    
    # Elementos del PDF
    elements = []
    styles = getSampleStyleSheet()
    
    # Título ajustado y reducido
    title = Paragraph("Lista de Gravedad Específica", 
                     styles['Heading1'].clone('Title', 
                                            alignment=1,  # Centrado
                                            fontSize=12,  # Tamaño reducido
                                            spaceAfter=10))  # Espacio después del título
    elements.append(title)
    elements.append(Paragraph("<br/>", styles['Normal']))  # Espacio reducido

    # Encabezados ajustados y reducidos
    headers = ['ID', 'Proyecto', 'Prospección', 'Tipo', 'Muestra', 
               'Prof. Ini', 'Prof. Fin', 'Prof. Prom', 
               'Grav. Esp', 'Área', 'Usuario']
    
    # Datos
    data = [headers]
    
    try:
        # Obtener queryset base
        gravedad_list = gravedad_especifica.objects.select_related(
            'id_proyecto', 'id_prospeccion', 'user'
        ).prefetch_related('id_muestra__muestreo_set').all()

        logger.debug(f"Registros iniciales: {gravedad_list.count()}, query: '{query}'")

        # Aplicar filtros si hay query
        if query:
            filtros = Q()
            try:
                query_numeric = float(query)
                filtros |= (
                    Q(profundidad_desde=query_numeric) |
                    Q(profundidad_hasta=query_numeric) |
                    Q(profundidad_promedio=query_numeric) |
                    Q(gravedad_especifica=query_numeric)
                )
            except ValueError:
                pass

            filtros |= (
                Q(id__icontains=query) |
                Q(id_proyecto__id__icontains=query) |
                Q(id_prospeccion__id_prospeccion__icontains=query) |
                Q(tipo_prospeccion__icontains=query) |
                Q(id_muestra__icontains=query) |
                Q(user__username__icontains=query)
            )

            gravedad_list = gravedad_list.filter(filtros)
        
        logger.debug(f"Registros después del filtro: {gravedad_list.count()}")

        # Construir las filas
        for gravedad in gravedad_list:
            try:
                muestreo = Muestreo.objects.filter(id_muestra=gravedad.id_muestra).first()
                
                row = [
                    str(gravedad.id) if gravedad.id is not None else '',
                    str(gravedad.id_proyecto.id) if gravedad.id_proyecto else '',
                    str(gravedad.id_prospeccion.id_prospeccion) if gravedad.id_prospeccion else '',
                    str(gravedad.tipo_prospeccion or ''),
                    str(gravedad.id_muestra or ''),
                    str(gravedad.profundidad_desde) if gravedad.profundidad_desde is not None else '',
                    str(gravedad.profundidad_hasta) if gravedad.profundidad_hasta is not None else '',
                    str(gravedad.profundidad_promedio) if gravedad.profundidad_promedio is not None else '',
                    str(gravedad.gravedad_especifica) if gravedad.gravedad_especifica is not None else '',
                    str(muestreo.area) if muestreo and hasattr(muestreo, 'area') else '',
                    str(gravedad.user.username) if gravedad.user else 'Sin usuario'
                ]
                data.append(row)
            except Exception as e:
                logger.error(f"Error al procesar registro {gravedad.id}: {str(e)}")
                continue

        # Crear tabla con tamaños ajustados
        table = Table(data, colWidths=[0.5*inch] + [0.8*inch]*10)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),    # Tamaño reducido para encabezados
            ('FONTSIZE', (0, 1), (-1, -1), 8),   # Tamaño de datos
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Padding reducido
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        doc.build(elements)
        return response

    except Exception as e:
        logger.error(f"Error en export_to_pdf_gravedad_especifica: {str(e)}")
        doc.build([Paragraph(f"Error al generar el reporte: {str(e)}", styles['Normal'])])
        return response

#Grficos Gravedad especifica
# Función de gráfico por área para gravedad específica
def generar_grafico_gravedad_area(df):
    areas_unicas = df['area'].unique()
    colores = {area: np.random.rand(3,) for area in areas_unicas}
    fig, ax = plt.subplots()
    for area in areas_unicas:
        datos_area = df[df['area'] == area]
        ax.scatter(
            datos_area['gravedad_especifica'],
            datos_area['profundidad_promedio'],
            color=colores[area],
            s=100,
            label=area,
            marker='s'
        )
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.invert_yaxis()
    ax.set_xlabel("Gravedad Específica")
    ax.set_ylabel("Profundidad Promedio (m)")
    ax.grid(True)
    plt.subplots_adjust(right=0.75)
    num_columns = (len(areas_unicas) + 24) // 25
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=num_columns)
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight', bbox_extra_artists=[legend])
    buffer.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

# Función de gráfico por ID de muestra para gravedad específica
def generar_grafico_gravedad_muestra(df):
    df['id_muestra'] = df['id_muestra'].astype(str)
    muestras_unicas = df['id_muestra'].unique()
    colores = {muestra: np.random.rand(3,) for muestra in muestras_unicas}
    fig, ax = plt.subplots()
    for muestra in muestras_unicas:
        datos_muestra = df[df['id_muestra'] == muestra]
        ax.scatter(
            datos_muestra['gravedad_especifica'],
            datos_muestra['profundidad_promedio'],
            color=colores[muestra],
            s=100,
            label=muestra,
            marker='s'
        )
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.invert_yaxis()
    ax.set_xlabel("Gravedad Específica")
    ax.set_ylabel("Profundidad Promedio (m)")
    ax.grid(True)
    plt.subplots_adjust(right=0.75)
    num_columns = (len(muestras_unicas) + 24) // 25
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=num_columns)
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight', bbox_extra_artists=[legend])
    buffer.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

# Vista para gráficos de gravedad específica
def graficos_gravedad_especifica(request):
    id_proyectos = request.GET.getlist('id_proyectos')
    tipos_prospeccion = request.GET.getlist('tipos_prospeccion')
    areas = request.GET.getlist('areas')
    id_prospecciones = request.GET.getlist('id_prospecciones')

    query = gravedad_especifica.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    if id_prospecciones:
        query = query.filter(id_prospeccion__in=id_prospecciones)

    proyectos = query.values('id_proyecto').distinct()
    tipos_prospeccion_inicial = query.values_list('tipo_prospeccion', flat=True).distinct().exclude(tipo_prospeccion__isnull=True)
    areas_inicial = query.values_list('area', flat=True).distinct().exclude(area__isnull=True).exclude(area='')
    id_prospecciones_inicial = query.values_list('id_prospeccion', flat=True).distinct().exclude(id_prospeccion__isnull=True)

    df = pd.DataFrame(list(query.values('gravedad_especifica', 'area', 'profundidad_promedio', 'id_muestra')))

    context = {
        'proyectos': proyectos,
        'tipos_prospeccion_inicial': tipos_prospeccion_inicial,
        'areas_inicial': areas_inicial,
        'id_prospecciones_inicial': id_prospecciones_inicial,
        'selected_id_proyectos': json.dumps(id_proyectos),
        'selected_tipos_prospeccion': json.dumps(tipos_prospeccion),
        'selected_areas': json.dumps(areas),
        'selected_id_prospecciones': json.dumps(id_prospecciones),
    }

    if df.empty:
        context['error'] = "No hay datos disponibles para los filtros seleccionados."
    else:
        context['image_base64_area'] = generar_grafico_gravedad_area(df)
        context['image_base64_muestra'] = generar_grafico_gravedad_muestra(df)

    return render(request, 'laboratorio/ensayos/gravedad_especifica/graficos_gravedad_especifica.html', context)

# Funciones auxiliares
def obtener_tipos_prospeccion_gravedad(request):
    id_proyectos = request.GET.get('id_proyectos')
    query = gravedad_especifica.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos.split(','))
    tipos_list = list(query.values_list('tipo_prospeccion', flat=True).distinct().exclude(tipo_prospeccion__isnull=True))
    return JsonResponse({'options': tipos_list}, safe=False)

def obtener_id_prospecciones_gravedad(request):
    id_proyectos = request.GET.get('id_proyectos')
    tipos_prospeccion = request.GET.get('tipos_prospeccion')
    areas = request.GET.get('areas')
    query = gravedad_especifica.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos.split(','))
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion.split(','))
    if areas:
        query = query.filter(area__in=areas.split(','))
    id_prospecciones_list = list(query.values_list('id_prospeccion', flat=True).distinct().exclude(id_prospeccion__isnull=True))
    return JsonResponse({'options': id_prospecciones_list}, safe=False)

def obtener_area_gravedad(request):
    id_prospecciones = request.GET.get('id_prospecciones')
    if id_prospecciones:
        query = gravedad_especifica.objects.filter(id_prospeccion__in=id_prospecciones.split(','))
        areas_list = list(query.values_list('area', flat=True).distinct().exclude(area__isnull=True).exclude(area=''))
        return JsonResponse({'options': areas_list})
    return JsonResponse({'options': []})


###USCS##################################################

logger = logging.getLogger(__name__)

@login_required
def agregar_uscs(request):
    proyectos_con_muestreo = Proyectos.objects.filter(muestreo__isnull=False).distinct()
    uscs_choices = uscs._meta.get_field('uscs').choices  # Obtener las opciones del modelo

    if request.method == 'POST':
        post_data = request.POST.copy()
        proyecto_id = post_data.get('id_proyecto')
        tipo_prospeccion = post_data.get('tipo_prospeccion')
        area = post_data.get('area')

        if proyecto_id:
            try:
                proyecto = Proyectos.objects.get(id=proyecto_id)
                post_data['id_proyecto'] = proyecto.id
            except Proyectos.DoesNotExist:
                post_data['id_proyecto'] = None

        id_prospecciones = post_data.getlist('id_prospeccion')
        muestras = post_data.getlist('id_muestra')
        uscs_values = post_data.getlist('uscs')
        profundidades_desde = post_data.getlist('profundidad_desde')
        profundidades_hasta = post_data.getlist('profundidad_hasta')
        errors = []

        for id_pros, muestra, uscs_val, desde, hasta in zip(id_prospecciones, muestras, uscs_values, profundidades_desde, profundidades_hasta):
            if not id_pros or not muestra or not uscs_val:
                errors.append(f"Falta ID de prospección, ID de muestra o clasificación USCS para una entrada.")
                continue
            
            try:
                prospeccion = Prospecciones.objects.get(id_prospeccion=id_pros)
                post_data['id_prospeccion'] = prospeccion.id_prospeccion
            except Prospecciones.DoesNotExist:
                errors.append(f"Prospección {id_pros} no encontrada.")
                continue

            try:
                uscs_obj = uscs(
                    id_proyecto=proyecto if proyecto_id else None,
                    tipo_prospeccion=tipo_prospeccion,
                    id_prospeccion=prospeccion,
                    id_muestra=muestra,
                    profundidad_desde=desde if desde else None,
                    profundidad_hasta=hasta if hasta else None,
                    profundidad_promedio=(float(desde) + float(hasta)) / 2 if desde and hasta else 0,
                    uscs=uscs_val,
                    area=area,
                    user=request.user
                )
                uscs_obj.save()
                logger.info(f"USCS creado: ID {uscs_obj.id}")
            except Exception as e:
                logger.error(f"Error al guardar USCS para muestra {muestra}: {e}")
                errors.append(f"Error al guardar muestra {muestra}: {e}")

        if errors:
            return render(request, 'laboratorio/ensayos/uscs/agregar_uscs.html', {
                'proyectos': proyectos_con_muestreo,
                'uscs_choices': uscs_choices,
                'errors': errors
            })
        return redirect('listar_uscs')

    return render(request, 'laboratorio/ensayos/uscs/agregar_uscs.html', {
        'proyectos': proyectos_con_muestreo,
        'uscs_choices': uscs_choices
    })
    
# 2. Listar USCS
@login_required
def listar_uscs(request):
    uscs_list = uscs.objects.all().order_by('id')  # Ordenar por 'id'
    query = request.GET.get('q', '')

    if query:
        uscs_model = apps.get_model('administrador', 'uscs')
        # Incluir campos de texto y numéricos
        campos = [field.name for field in uscs_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField, DecimalField, FloatField, ForeignKey))]
        query_filter = Q()
        
        # Intentar convertir el query a float para búsquedas numéricas
        try:
            query_numeric = float(query)
            numeric_search = True
        except ValueError:
            numeric_search = False

        for field in campos:
            field_instance = uscs_model._meta.get_field(field)
            if isinstance(field_instance, (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            elif isinstance(field_instance, ForeignKey):
                related_model = field_instance.related_model
                related_fields = [f"{field}__{related_field.name}" for related_field in related_model._meta.get_fields() if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    query_filter |= Q(**{f"{related_field}__icontains": query})
            elif isinstance(field_instance, (DecimalField, FloatField)) and numeric_search:
                # Para campos numéricos, usar coincidencia exacta
                query_filter |= Q(**{f"{field}": query_numeric})
            else:
                # Para campos de texto
                query_filter |= Q(**{f"{field}__icontains": query})
        
        uscs_list = uscs_list.filter(query_filter)

    paginator = Paginator(uscs_list, 1000)  # 1000 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Si es una solicitud AJAX (opcional)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'laboratorio/ensayos/uscs/uscs_table.html', {'page_obj': page_obj})
    
    return render(request, 'laboratorio/ensayos/uscs/listar_uscs.html', {
        'page_obj': page_obj,
        'query': query
    })

# 3. Editar USCS
@login_required
def editar_uscs(request, id):
    uscs_obj = get_object_or_404(uscs, id=id)
    proyectos = Proyectos.objects.all()
    if request.method == 'POST':
        form = UscsForm(request.POST, instance=uscs_obj)
        if form.is_valid():
            try:
                uscs_obj = form.save()
                logger.info(f"USCS editado: ID {uscs_obj.id}")
                return redirect('listar_uscs')
            except Exception as e:
                logger.error(f"Error al editar USCS {uscs_obj.id}: {e}")
                form.add_error(None, f"Error al editar: {e}")
    else:
        form = UscsForm(instance=uscs_obj)
    return render(request, 'laboratorio/ensayos/uscs/editar_uscs.html', {'form': form, 'uscs': uscs_obj, 'proyectos': proyectos})



@login_required
def ver_uscs(request, id):
    uscs = get_object_or_404(uscs, id=id)
    return render(request, 'laboratorio/ensayos/uscs/ver_uscs.html', {'uscs': uscs})



# 4. Eliminar USCS
@login_required
def eliminar_uscs(request, id):
    uscs_obj = get_object_or_404(uscs, id=id)
    if request.method == 'POST':
        uscs_obj.delete()
        return redirect('listar_uscs')
    return render(request, 'laboratorio/ensayos/uscs/eliminar_uscs.html', {'uscs': uscs_obj})

# 5. Exportar a Excel USCS
def export_to_excel_uscs(request):
    query = request.GET.get('q', '')
    headers = ['ID', 'ID Proyecto', 'ID Prospección', 'Tipo Prospección', 'ID Muestra', 'USCS', 'Área', 'Usuario']

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="uscs_filtrado.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "USCS Filtrado"
    ws.append(headers)

    uscs_list = uscs.objects.all()
    if query:
        uscs_list = uscs_list.filter(
            Q(id_prospeccion__id_prospeccion__icontains=query) |
            Q(id_muestra__icontains=query) |
            Q(uscs__icontains=query)
        )

    for uscs_obj in uscs_list:
        row = [
            uscs_obj.id,
            str(uscs_obj.id_proyecto),
            str(uscs_obj.id_prospeccion),
            uscs_obj.tipo_prospeccion,
            uscs_obj.id_muestra,
            uscs_obj.uscs,
            uscs_obj.area,
            uscs_obj.user.username if uscs_obj.user else 'Sin usuario'
        ]
        ws.append(row)

    wb.save(response)
    return response

# 6. Exportar a PDF USCS
def export_to_pdf_uscs(request):
    query = request.GET.get('q', '')
    headers = ['ID', 'ID Proyecto', 'ID Prospección', 'Tipo Prospección', 'ID Muestra', 'USCS', 'Área', 'Usuario']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="uscs_filtrado.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Reporte de Clasificaciones USCS Filtradas")
    p.drawString(100, 730, " | ".join(headers))

    uscs_list = uscs.objects.all()
    if query:
        uscs_list = uscs_list.filter(
            Q(id_prospeccion__id_prospeccion__icontains=query) |
            Q(id_muestra__icontains=query) |
            Q(uscs__icontains=query)
        )

    y = 710
    for uscs_obj in uscs_list:
        row = [
            str(uscs_obj.id),
            str(uscs_obj.id_proyecto),
            str(uscs_obj.id_prospeccion),
            uscs_obj.tipo_prospeccion,
            uscs_obj.id_muestra,
            uscs_obj.uscs,
            uscs_obj.area,
            uscs_obj.user.username if uscs_obj.user else 'Sin usuario'
        ]
        p.drawString(100, y, " | ".join(row))
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    return response

# 7. Gráficos USCS

# Vista para gráficos USCS
def graficos_uscs(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    tipos_prospeccion = request.GET.getlist('tipo_prospeccion')
    areas = request.GET.getlist('area')
    id_prospecciones = request.GET.getlist('id_prospeccion')
    
    query = uscs.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    if id_prospecciones:
        query = query.filter(id_prospeccion__in=id_prospecciones)
    
    proyectos = query.values('id_proyecto').distinct()
    tipos_prospeccion_inicial = (query.values_list('tipo_prospeccion', flat=True)
                                 .distinct().exclude(tipo_prospeccion__isnull=True).exclude(tipo_prospeccion=''))
    areas_inicial = (query.values_list('area', flat=True)
                     .distinct().exclude(area__isnull=True).exclude(area=''))
    id_prospecciones_inicial = (query.values_list('id_prospeccion', flat=True)
                                .distinct().exclude(id_prospeccion__isnull=True).exclude(id_prospeccion=''))
    
    df = pd.DataFrame.from_records(query.values('id_proyecto', 'id_prospeccion', 'id_muestra', 'uscs', 'area'))
    
    context = {
        'proyectos': proyectos,
        'tipos_prospeccion_inicial': tipos_prospeccion_inicial,
        'areas_inicial': areas_inicial,
        'id_prospecciones_inicial': id_prospecciones_inicial,
        'selected_id_proyectos': json.dumps(id_proyectos),
        'selected_tipos_prospeccion': json.dumps(tipos_prospeccion),
        'selected_areas': json.dumps(areas),
        'selected_id_prospecciones': json.dumps(id_prospecciones),
    }
    
    if df.empty:
        context['error'] = "No hay datos para graficar."
        return render(request, 'laboratorio/ensayos/uscs/graficos_uscs.html', context)
    
    # Gráfico 1: Distribución porcentual de clasificaciones USCS (anillo)
    def generar_grafico_distribucion_uscs(df):
        uscs_counts = df['uscs'].value_counts(normalize=True) * 100
        labels = uscs_counts.index
        sizes = uscs_counts.values
        colors = [np.random.rand(3,) for _ in range(len(labels))]  # Colores aleatorios como en humedad
        
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                                          startangle=90, wedgeprops=dict(width=0.3, edgecolor='white'))
        ax.grid(True)  # Grilla como en humedad
        plt.subplots_adjust(right=0.75)  # Márgenes como en humedad
        num_columns = (len(labels) + 24) // 25  # Cálculo de columnas como en humedad
        legend = ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), ncol=num_columns)
        ax.set_title("Distribución Porcentual de Clasificaciones USCS")
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight', bbox_extra_artists=[legend])
        buffer.seek(0)
        plt.close()
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Gráfico 2: Clasificaciones por área (barras apiladas)
    def generar_grafico_uscs_por_area(df):
        pivot = df.pivot_table(index='area', columns='uscs', aggfunc='size', fill_value=0)
        colors = [np.random.rand(3,) for _ in range(len(pivot.columns))]  # Colores aleatorios como en humedad
        
        fig, ax = plt.subplots()
        pivot.plot(kind='bar', stacked=True, ax=ax, color=colors, edgecolor='white', linewidth=0.5)
        ax.set_xlabel("Área")
        ax.set_ylabel("Cantidad")
        ax.grid(True)  # Grilla como en humedad
        plt.subplots_adjust(right=0.75)  # Márgenes como en humedad
        num_columns = (len(pivot.columns) + 24) // 25  # Cálculo de columnas como en humedad
        legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=num_columns)
        ax.set_title("Clasificaciones USCS por Área")
        plt.xticks(rotation=45, ha='right')
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=85, bbox_inches='tight', bbox_extra_artists=[legend])
        buffer.seek(0)
        plt.close()
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    image_base64_distribucion = generar_grafico_distribucion_uscs(df)
    image_base64_area = generar_grafico_uscs_por_area(df)
    
    context.update({
        'image_base64_distribucion': image_base64_distribucion,
        'image_base64_area': image_base64_area,
    })
    return render(request, 'laboratorio/ensayos/uscs/graficos_uscs.html', context)



from django.http import JsonResponse
from .models import Muestreo, Prospecciones

# Obtener tipos de prospección desde Muestreo
def obtener_tipos_prospeccion_muestreo(request):
    id_proyecto = request.GET.get('id_proyecto')
    tipos = Muestreo.objects.all()
    if id_proyecto:
        tipos = tipos.filter(id_proyecto=id_proyecto)
    tipos_list = list(tipos.values_list('tipo_prospeccion', flat=True)
                     .distinct()
                     .exclude(tipo_prospeccion__isnull=True)
                     .exclude(tipo_prospeccion=''))
    return JsonResponse({'options': tipos_list}, safe=False)

# Obtener IDs de prospección desde Muestreo
def obtener_id_prospecciones_muestreo(request):
    id_proyecto = request.GET.get('id_proyecto')
    tipo_prospeccion = request.GET.get('tipo_prospeccion')
    query = Muestreo.objects.all()
    if id_proyecto:
        query = query.filter(id_proyecto=id_proyecto)
    if tipo_prospeccion:
        query = query.filter(tipo_prospeccion=tipo_prospeccion)
    id_prospecciones_list = list(query.values_list('id_prospeccion__id_prospeccion', flat=True)
                                 .distinct()
                                 .exclude(id_prospeccion__isnull=True))
    return JsonResponse({'options': id_prospecciones_list}, safe=False)

# Obtener área desde Muestreo
def obtener_area_muestreo(request):
    prospeccion_id = request.GET.get('prospeccion_id')
    if prospeccion_id:
        try:
            muestreo = Muestreo.objects.filter(id_prospeccion__id_prospeccion=prospeccion_id).first()
            if muestreo:
                return JsonResponse({'area': muestreo.area})
        except Muestreo.DoesNotExist:
            pass
    return JsonResponse({'area': ''})

# Obtener IDs de muestra desde Muestreo
def obtener_id_muestras_muestreo(request):
    id_prospeccion = request.GET.get('id_prospeccion')
    muestras = Muestreo.objects.all()
    if id_prospeccion:
        muestras = muestras.filter(id_prospeccion__id_prospeccion=id_prospeccion)
    muestras_list = list(muestras.values_list('id_muestra', flat=True)
                        .distinct()
                        .exclude(id_muestra__isnull=True)
                        .exclude(id_muestra=''))
    return JsonResponse({'options': muestras_list}, safe=False)


def obtener_profundidades_muestreo(request):
    id_muestra = request.GET.get('id_muestra')
    if id_muestra:
        try:
            muestreo = Muestreo.objects.get(id_muestra=id_muestra)
            return JsonResponse({
                'profundidad_desde': str(muestreo.profundidad_desde) if muestreo.profundidad_desde else '',
                'profundidad_hasta': str(muestreo.profundidad_hasta) if muestreo.profundidad_hasta else ''
            })
        except Muestreo.DoesNotExist:
            return JsonResponse({'profundidad_desde': '', 'profundidad_hasta': ''})
    return JsonResponse({'profundidad_desde': '', 'profundidad_hasta': ''})




#### HUMEDAD ##############################################

# Funciones de humedad
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Proyectos, Muestreo  # Asegúrate de importar tus modelos
from .forms import HumedadForm  # Asegúrate de tener este formulario definido
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Proyectos, Muestreo, Humedad, Prospecciones

logger = logging.getLogger(__name__)

@login_required
def agregar_humedad(request):
    # Filtrar proyectos que tienen registros en Muestreo
    proyectos_con_muestreo = Proyectos.objects.filter(muestreo__isnull=False).distinct()

    if request.method == 'POST':
        post_data = request.POST.copy()
        proyecto_id = post_data.get('id_proyecto')
        tipo_prospeccion = post_data.get('tipo_prospeccion')
        area = post_data.get('area')

        # Validar y asignar proyecto
        if proyecto_id:
            try:
                proyecto = Proyectos.objects.get(id=proyecto_id)
                post_data['id_proyecto'] = proyecto.id
            except Proyectos.DoesNotExist:
                post_data['id_proyecto'] = None

        # Manejar múltiples muestras y valores de humedad
        id_prospecciones = post_data.getlist('id_prospeccion')  # Lista de prospecciones por fila
        muestras = post_data.getlist('id_muestra')
        humedades = post_data.getlist('humedad')
        profundidades_desde = post_data.getlist('profundidad_desde')
        profundidades_hasta = post_data.getlist('profundidad_hasta')
        errors = []

        for id_pros, muestra, humedad_val, desde, hasta in zip(id_prospecciones, muestras, humedades, profundidades_desde, profundidades_hasta):
            if not id_pros or not muestra or not humedad_val:
                errors.append(f"Falta ID de prospección, ID de muestra o valor de humedad para una entrada.")
                continue
            
            # Validar y asignar prospección
            try:
                prospeccion = Prospecciones.objects.get(id_prospeccion=id_pros)
                post_data['id_prospeccion'] = prospeccion.id_prospeccion
            except Prospecciones.DoesNotExist:
                errors.append(f"Prospección {id_pros} no encontrada.")
                continue

            post_data['id_muestra'] = muestra
            post_data['humedad'] = humedad_val
            post_data['tipo_prospeccion'] = tipo_prospeccion
            post_data['area'] = area

            # Crear instancia de Humedad manualmente
            try:
                humedad_obj = Humedad(
                    id_proyecto=proyecto if proyecto_id else None,
                    tipo_prospeccion=tipo_prospeccion,
                    id_prospeccion=prospeccion,
                    area=area,
                    humedad=humedad_val,
                    profundidad_promedio=(float(desde) + float(hasta)) / 2 if desde and hasta else 0,
                    user=request.user
                )
                humedad_obj.save()
                logger.info(f"Humedad creada: ID {humedad_obj.id}")
            except Exception as e:
                logger.error(f"Error al guardar humedad para muestra {muestra}: {e}")
                errors.append(f"Error al guardar muestra {muestra}: {e}")

        if errors:
            return render(request, 'laboratorio/ensayos/humedad/agregar_humedad.html', {
                'proyectos': proyectos_con_muestreo,
                'errors': errors
            })
        return redirect('listar_humedad')

    return render(request, 'laboratorio/ensayos/humedad/agregar_humedad.html', {
        'proyectos': proyectos_con_muestreo
    })

def listar_humedad(request):
    humedades = Humedad.objects.all().order_by('id')
    query = request.GET.get('q', '')
    if query:
        humedades = humedades.filter(
            Q(id_proyecto__id__icontains=query) |
            Q(id_prospeccion__id_prospeccion__icontains=query) |
            Q(tipo_prospeccion__icontains=query) |
            Q(humedad__icontains=query) |
            Q(profundidad_promedio__icontains=query) |
            Q(area__icontains=query)
        )
    paginator = Paginator(humedades, 1000)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'laboratorio/ensayos/humedad/humedad_table.html', {'page_obj': page_obj})
    return render(request, 'laboratorio/ensayos/humedad/listar_humedad.html', {'page_obj': page_obj, 'query': query})

from django.http import HttpResponse
from openpyxl import Workbook

def export_to_excel_humedad(request):
    # Obtener parámetros del request
    query = request.GET.get('q', '')
    headers_str = request.GET.get('headers', '')
    headers = headers_str.split(',') if headers_str else ['ID', 'Tipo Prospección', 'ID Proyecto', 'ID Prospección', 'Humedad', 'Profundidad Promedio', 'Área']

    # Crear respuesta para Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="humedad_filtrada.xlsx"'

    # Crear el libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Humedad Filtrada"

    # Agregar encabezados dinámicos
    ws.append(headers)

    # Obtener datos filtrados
    humedades = Humedad.objects.all()
    if query:
        humedades = humedades.filter(id_prospeccion__id_prospeccion__icontains=query)

    # Mapear campos según encabezados
    for humedad in humedades:
        row = []
        for header in headers:
            if header == 'ID':
                value = humedad.id
            elif header == 'Tipo Prospección':
                value = humedad.tipo_prospeccion
            elif header == 'ID Proyecto':
                value = str(humedad.id_proyecto)
            elif header == 'ID Prospección':
                value = str(humedad.id_prospeccion)
            elif header == 'Humedad (%)':
                value = humedad.humedad
            elif header == 'Profundidad Promedio (m)':
                value = humedad.profundidad_promedio
            elif header == 'Área':
                value = humedad.area
            elif header == 'Usuario':
                value = humedad.user.username if humedad.user else 'Sin usuario'
            else:
                value = '-'  # Valor por defecto si el encabezado no coincide
            row.append(value)
        ws.append(row)

    # Guardar y devolver respuesta
    wb.save(response)
    return response

def ver_humedad(request, id):
    humedad = get_object_or_404(Humedad, id=id)
    return render(request, 'laboratorio/ensayos/humedad/ver_humedad.html', {'humedad': humedad})

from django.http import HttpResponse
from reportlab.pdfgen import canvas

def export_to_pdf_humedad(request):
    # Obtener parámetros del request
    query = request.GET.get('q', '')
    headers_str = request.GET.get('headers', '')
    headers = headers_str.split(',') if headers_str else ['ID', 'Tipo Prospección', 'ID Proyecto', 'ID Prospección', 'Humedad', 'Profundidad Promedio', 'Área']

    # Crear respuesta para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="humedad_filtrada.pdf"'

    # Crear el objeto PDF
    p = canvas.Canvas(response)

    # Agregar título y encabezados dinámicos
    p.drawString(100, 750, "Reporte de Humedad Filtrada")
    p.drawString(100, 730, " | ".join(headers))

    # Obtener datos filtrados
    humedades = Humedad.objects.all()
    if query:
        humedades = humedades.filter(id_prospeccion__id_prospeccion__icontains=query)

    # Rellenar datos
    y = 710
    for humedad in humedades:
        row = []
        for header in headers:
            if header == 'ID':
                value = str(humedad.id)
            elif header == 'Tipo Prospección':
                value = humedad.tipo_prospeccion
            elif header == 'ID Proyecto':
                value = str(humedad.id_proyecto)
            elif header == 'ID Prospección':
                value = str(humedad.id_prospeccion)
            elif header == 'Humedad (%)':
                value = str(humedad.humedad)
            elif header == 'Profundidad Promedio (m)':
                value = str(humedad.profundidad_promedio)
            elif header == 'Área':
                value = humedad.area
            elif header == 'Usuario':
                value = humedad.user.username if humedad.user else 'Sin usuario'
            else:
                value = '-'
            row.append(value)
        p.drawString(100, y, " | ".join(row))
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    # Finalizar el PDF
    p.showPage()
    p.save()
    return response

@login_required
def editar_humedad(request, id):
    humedad = get_object_or_404(Humedad, id=id)
    proyectos = Proyectos.objects.all()
    if request.method == 'POST':
        form = HumedadForm(request.POST, instance=humedad)
        if form.is_valid():
            try:
                humedad = form.save()
                logger.info(f"Humedad editada: ID {humedad.id}, Área: {humedad.area}")
                return redirect('listar_humedad')
            except Exception as e:
                logger.error(f"Error al editar humedad {humedad.id}: {e}")
                form.add_error(None, f"Error al editar: {e}")
    else:
        form = HumedadForm(instance=humedad)
    return render(request, 'laboratorio/ensayos/humedad/editar_humedad.html', {'form': form, 'humedad': humedad, 'proyectos': proyectos})


def eliminar_humedad(request, id):
    humedad = get_object_or_404(Humedad, id=id)
    if request.method == 'POST':
        humedad.delete()
        return redirect('listar_humedad')
    return render(request, 'laboratorio/ensayos/humedad/eliminar_humedad.html', {'humedad': humedad})


# Funciones de gráficos por proyecto
def generar_grafico_humedad_area(df):
    areas_unicas = df['area'].unique()
    colores = {area: np.random.rand(3,) for area in areas_unicas}
    fig, ax = plt.subplots()
    for area in areas_unicas:
        datos_area = df[df['area'] == area]
        ax.scatter(
            datos_area['humedad'],
            datos_area['profundidad_promedio'],
            color=colores[area],
            s=100,
            label=area,
            marker='+'
        )
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.invert_yaxis()
    ax.set_xlabel("Humedad (%)")
    ax.set_ylabel("Profundidad (m)")
    ax.grid(True)
    plt.subplots_adjust(right=0.75)
    num_columns = (len(areas_unicas) + 24) // 25
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=num_columns)
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight', bbox_extra_artists=[legend])
    buffer.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

# Funciones de gráficos por prospeccion
def generar_grafico_humedad_prospeccion(df):
    df['id_prospeccion'] = df['id_prospeccion'].astype(str)
    df['id_prospeccion_unico'] = df.groupby('id_prospeccion').cumcount() + 1
    df['etiqueta'] = df['id_prospeccion'] + '-' + df['id_prospeccion_unico'].astype(str)
    prospecciones_unicas = df['etiqueta'].unique()
    colores = {prospeccion: np.random.rand(3,) for prospeccion in prospecciones_unicas}
    fig, ax = plt.subplots()
    for prospeccion in prospecciones_unicas:
        datos_prospeccion = df[df['etiqueta'] == prospeccion]
        ax.scatter(
            datos_prospeccion['humedad'],
            datos_prospeccion['profundidad_promedio'],
            color=colores[prospeccion],
            s=100,
            label=prospeccion,
            marker='+'
        )
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.invert_yaxis()
    ax.set_xlabel("Humedad (%)")
    ax.set_ylabel("Profundidad (m)")
    ax.grid(True)
    plt.subplots_adjust(right=0.75)
    num_columns = (len(prospecciones_unicas) + 24) // 25
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=num_columns)
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight', bbox_extra_artists=[legend])
    buffer.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64


# Funciones de gráficos
def graficos_humedad(request):
    id_proyectos = request.GET.getlist('id_proyectos')
    tipos_prospeccion = request.GET.getlist('tipos_prospeccion')
    areas = request.GET.getlist('areas')
    id_prospecciones = request.GET.getlist('id_prospecciones')
    query = Humedad.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    if id_prospecciones:
        query = query.filter(id_prospeccion__in=id_prospecciones)
    proyectos = query.values('id_proyecto').distinct()
    tipos_prospeccion_inicial = (query.values_list('tipo_prospeccion', flat=True)
                                 .distinct().exclude(tipo_prospeccion__isnull=True).exclude(tipo_prospeccion=''))
    areas_inicial = (query.values_list('area', flat=True)
                     .distinct().exclude(area__isnull=True).exclude(area=''))
    id_prospecciones_inicial = (query.values_list('id_prospeccion', flat=True)
                                .distinct().exclude(id_prospeccion__isnull=True).exclude(id_prospeccion=''))
    humedades = Humedad.objects.all()
    if id_proyectos:
        humedades = humedades.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        humedades = humedades.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        humedades = humedades.filter(area__in=areas)
    if id_prospecciones:
        humedades = humedades.filter(id_prospeccion__in=id_prospecciones)
    df = pd.DataFrame.from_records(humedades.values('id_proyecto', 'id_prospeccion', 'humedad', 'profundidad_promedio', 'area'))
    if df.empty:
        context = {
            'error': "No hay datos para graficar.",
            'proyectos': proyectos,
            'tipos_prospeccion_inicial': tipos_prospeccion_inicial,
            'areas_inicial': areas_inicial,
            'id_prospecciones_inicial': id_prospecciones_inicial,
            'selected_id_proyectos': json.dumps(id_proyectos),
            'selected_tipos_prospeccion': json.dumps(tipos_prospeccion),
            'selected_areas': json.dumps(areas),
            'selected_id_prospecciones': json.dumps(id_prospecciones),
        }
        return render(request, 'laboratorio/ensayos/humedad/graficos_humedad.html', context)
    image_base64_area = generar_grafico_humedad_area(df)
    image_base64_prospeccion = generar_grafico_humedad_prospeccion(df)
    context = {
        'image_base64_area': image_base64_area,
        'image_base64_prospeccion': image_base64_prospeccion,
        'proyectos': proyectos,
        'tipos_prospeccion_inicial': tipos_prospeccion_inicial,
        'areas_inicial': areas_inicial,
        'id_prospecciones_inicial': id_prospecciones_inicial,
        'selected_id_proyectos': json.dumps(id_proyectos),
        'selected_tipos_prospeccion': json.dumps(tipos_prospeccion),
        'selected_areas': json.dumps(areas),
        'selected_id_prospecciones': json.dumps(id_prospecciones),
    }
    return render(request, 'laboratorio/ensayos/humedad/graficos_humedad.html', context)


##Obtener funciones API para humedad
# Obtener tipos de prospección para Humedad
def obtener_tipos_prospeccion_humedad(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    tipos = Humedad.objects.all()
    if id_proyectos:
        tipos = tipos.filter(id_proyecto__in=id_proyectos)
    tipos_list = list(tipos.values_list('tipo_prospeccion', flat=True)
                     .distinct()
                     .exclude(tipo_prospeccion__isnull=True)
                     .exclude(tipo_prospeccion=''))
    print(f"Tipos de prospección para id_proyectos={id_proyectos}: {tipos_list}")
    return JsonResponse({'options': tipos_list}, safe=False)

# Obtener áreas para Humedad
def obtener_areas_humedad(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    areas = Humedad.objects.all()
    if id_proyectos:
        areas = areas.filter(id_proyecto__in=id_proyectos)
    areas_list = list(areas.values_list('area', flat=True)
                     .distinct()
                     .exclude(area__isnull=True)
                     .exclude(area=''))
    print(f"Áreas para id_proyectos={id_proyectos}: {areas_list}")
    return JsonResponse({'options': areas_list}, safe=False)

# Obtener IDs de prospección para Humedad
def obtener_id_prospecciones_humedad(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    tipos_prospeccion = request.GET.getlist('tipo_prospeccion')
    areas = request.GET.getlist('area')
    query = Humedad.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    id_prospecciones_list = list(query.values_list('id_prospeccion', flat=True)
                                .distinct()
                                .exclude(id_prospeccion__isnull=True)
                                .exclude(id_prospeccion=''))
    print(f"IDs de prospección para id_proyectos={id_proyectos}, tipos={tipos_prospeccion}, áreas={areas}: {id_prospecciones_list}")
    return JsonResponse({'options': id_prospecciones_list}, safe=False)

# Obtener proyectos para Humedad
def obtener_id_proyecto_humedad(request):
    tipos_prospeccion = request.GET.getlist('tipo_prospeccion')
    areas = request.GET.getlist('area')
    id_prospecciones = request.GET.getlist('id_prospeccion')
    query = Humedad.objects.all()
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    if id_prospecciones:
        query = query.filter(id_prospeccion__in=id_prospecciones)
    proyectos_list = list(query.values_list('id_proyecto', flat=True)
                         .distinct()
                         .exclude(id_proyecto__isnull=True)
                         .exclude(id_proyecto=''))
    print(f"Proyectos para tipos={tipos_prospeccion}, áreas={areas}, id_prospecciones={id_prospecciones}: {proyectos_list}")
    return JsonResponse({'options': proyectos_list}, safe=False)



#### GRANULOMETRIA ##############################################

# Funciones de granulometría
@login_required
def agregar_granulometria(request):
    proyectos = Proyectos.objects.all()
    if request.method == 'POST':
        post_data = request.POST.copy()
        proyecto_id = post_data.get('id_proyecto')
        if proyecto_id:
            try:
                proyecto = Proyectos.objects.get(id=proyecto_id)
                post_data['id_proyecto'] = proyecto
            except Proyectos.DoesNotExist:
                post_data['id_proyecto'] = None
        
        form = GranulometriaForm(post_data)
        if form.is_valid():
            try:
                granulometria = form.save(commit=False)
                granulometria.user = request.user
                granulometria.save()
                print(f"Granulometría creada: ID {granulometria.id}")  # Depuración
                return redirect('listar_granulometria')
            except Exception as e:
                print(f"Error al guardar granulometría: {e}")  # Depuración
                form.add_error(None, f"Error al guardar: {e}")
        else:
            print("Formulario no válido:", form.errors)  # Depuración
    else:
        form = GranulometriaForm()
    return render(request, 'laboratorio/ensayos/granulometria/agregar_granulometria.html', {'form': form, 'proyectos': proyectos})

#listar granulometrtia
def listar_granulometria(request):
    granulometrias = Granulometria.objects.all().order_by('id')
    query = request.GET.get('q', '')
    if query:
        granulometrias = granulometrias.filter(
            Q(id_proyecto__id__icontains=query) |
            Q(id_prospeccion__id_prospeccion__icontains=query) |
            Q(tipo_prospeccion__icontains=query)
        )
    paginator = Paginator(granulometrias, 1000)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'laboratorio/ensayos/granulometria/granulometria_table.html', {'page_obj': page_obj})
    return render(request, 'laboratorio/ensayos/granulometria/listar_granulometria.html', {'page_obj': page_obj, 'query': query})

def export_to_excel_granulometria(request):
    query = request.GET.get('q', '')
    headers_str = request.GET.get('headers', '')
    headers = headers_str.split(',') if headers_str else []

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="granulometria_filtrada.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Granulometria Filtrada"
    ws.append(headers)

    granulometrias = Granulometria.objects.all()
    if query:
        granulometrias = granulometrias.filter(id_prospeccion__id_prospeccion__icontains=query)

    for granulometria in granulometrias:
        row = []
        for header in headers:
            if header == 'ID Proyecto':
                value = str(granulometria.id_proyecto.id)
            elif header == 'ID Prospección':
                value = str(granulometria.id_prospeccion.id_prospeccion)
            elif header == 'Tipo Prospección':
                value = granulometria.tipo_prospeccion
            elif header == '0.075 mm':
                value = granulometria.n_0075
            elif header == '0.110 mm':
                value = granulometria.n_0110
            elif header == '0.250 mm':
                value = granulometria.n_0250
            elif header == '0.420 mm':
                value = granulometria.n_0420
            elif header == '0.840 mm':
                value = granulometria.n_0840
            elif header == '2.000 mm':
                value = granulometria.n_2000
            elif header == '4.760 mm':
                value = granulometria.n_4760
            elif header == '9.520 mm':
                value = granulometria.n_9520
            elif header == '19.000 mm':
                value = granulometria.n_19000
            elif header == '25.400 mm':
                value = granulometria.n_25400
            elif header == '38.100 mm':
                value = granulometria.n_38100
            elif header == '50.800 mm':
                value = granulometria.n_50800
            elif header == '63.500 mm':
                value = granulometria.n_63500
            elif header == '75.000 mm':
                value = granulometria.n_75000
            elif header == 'Área':
                value = granulometria.area
            elif header == 'Usuario':
                value = granulometria.user.username if granulometria.user else 'Sin usuario'
            else:
                value = '-'
            row.append(value)
        ws.append(row)

    wb.save(response)
    return response



def export_to_pdf_granulometria(request):
    # Obtener parámetros del request
    query = request.GET.get('q', '')
    headers_str = request.GET.get('headers', '')
    headers = headers_str.split(',') if headers_str else [
        'ID Proyecto', 'ID Prospección', 'Tipo Prospección', '0.075 mm', '0.110 mm', '0.250 mm',
        '0.420 mm', '0.840 mm', '2.000 mm', '4.760 mm', '9.520 mm', '19.000 mm', '25.400 mm',
        '38.100 mm', '50.800 mm', '63.500 mm', '75.000 mm', 'Área', 'Usuario'
    ]

    # Crear respuesta para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="granulometria_filtrada.pdf"'

    # Crear el objeto PDF
    p = canvas.Canvas(response)

    # Agregar título y encabezados dinámicos
    p.drawString(100, 750, "Reporte de Granulometría Filtrada")
    p.drawString(100, 730, " | ".join(headers))

    # Obtener datos filtrados
    granulometrias = Granulometria.objects.all()
    if query:
        granulometrias = granulometrias.filter(id_prospeccion__id_prospeccion__icontains=query)

    # Rellenar datos
    y = 710
    for granulometria in granulometrias:
        row = []
        for header in headers:
            if header == 'ID Proyecto':
                value = str(granulometria.id_proyecto.id)
            elif header == 'ID Prospección':
                value = str(granulometria.id_prospeccion.id_prospeccion)
            elif header == 'Tipo Prospección':
                value = granulometria.tipo_prospeccion
            elif header == '0.075 mm':
                value = str(granulometria.n_0075)
            elif header == '0.110 mm':
                value = str(granulometria.n_0110)
            elif header == '0.250 mm':
                value = str(granulometria.n_0250)
            elif header == '0.420 mm':
                value = str(granulometria.n_0420)
            elif header == '0.840 mm':
                value = str(granulometria.n_0840)
            elif header == '2.000 mm':
                value = str(granulometria.n_2000)
            elif header == '4.760 mm':
                value = str(granulometria.n_4760)
            elif header == '9.520 mm':
                value = str(granulometria.n_9520)
            elif header == '19.000 mm':
                value = str(granulometria.n_19000)
            elif header == '25.400 mm':
                value = str(granulometria.n_25400)
            elif header == '38.100 mm':
                value = str(granulometria.n_38100)
            elif header == '50.800 mm':
                value = str(granulometria.n_50800)
            elif header == '63.500 mm':
                value = str(granulometria.n_63500)
            elif header == '75.000 mm':
                value = str(granulometria.n_75000)
            elif header == 'Área':
                value = granulometria.area
            elif header == 'Usuario':
                value = granulometria.user.username if granulometria.user else 'Sin usuario'
            else:
                value = '-'
            row.append(value)
        text = " | ".join(row)
        p.drawString(100, y, text[:500])  # Limitar longitud para evitar desbordamiento
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    # Finalizar el PDF
    p.showPage()
    p.save()
    return response

#ver granulometria
def ver_granulometria(request, id):
    granulometria = get_object_or_404(Granulometria, id=id)
    return render(request, 'laboratorio/ensayos/granulometria/ver_granulometria.html', {'granulometria': granulometria})

#editar granulometria
@login_required
def editar_granulometria(request, id):
    granulometria = get_object_or_404(Granulometria, id=id)
    proyectos = Proyectos.objects.all()
    if request.method == 'POST':
        form = GranulometriaForm(request.POST, instance=granulometria)
        if form.is_valid():
            try:
                granulometria = form.save()
                logger.info(f"Granulometría editada: ID {granulometria.id}, Área: {granulometria.area}")
                return redirect('listar_granulometria')
            except Exception as e:
                logger.error(f"Error al editar granulometría {granulometria.id}: {e}")
                form.add_error(None, f"Error al editar: {e}")
    else:
        form = GranulometriaForm(instance=granulometria)
    return render(request, 'laboratorio/ensayos/granulometria/editar_granulometria.html', {'form': form, 'granulometria': granulometria, 'proyectos': proyectos})

#eliminar granulometria
def eliminar_granulometria(request, id):
    granulometria = get_object_or_404(Granulometria, id=id)
    if request.method == 'POST':
        granulometria.delete()
        return redirect('listar_granulometria')
    return render(request, 'laboratorio/ensayos/granulometria/eliminar_granulometria.html', {'granulometria': granulometria})

# Funciones de graficos granulometría por proyecto
def generar_grafico_granulometria_area(df):
    if 'id_prospeccion' not in df.columns:
        raise KeyError("La columna 'id_prospeccion' no está presente en los datos iniciales.")
    df['id_proyecto'] = df['id_proyecto'].astype(str)
    df['etiqueta'] = df['id_proyecto']
    proyectos_unicos = df['etiqueta'].unique()
    colores = {proyecto: np.random.rand(3,) for proyecto in proyectos_unicos}
    fig, ax = plt.subplots()
    x_values = np.array([0.075, 0.110, 0.250, 0.420, 0.840, 2.000, 4.760, 9.520, 19.000, 25.400, 38.100, 50.800, 63.500, 75.000])
    for proyecto in proyectos_unicos:
        datos_proyecto = df[df['etiqueta'] == proyecto]
        for i in range(len(datos_proyecto)):
            y_values = datos_proyecto.iloc[i, 2:16].values
            sorted_indices = np.argsort(x_values)[::-1]
            x_values_sorted = x_values[sorted_indices]
            y_values_sorted = y_values[sorted_indices]
            ax.plot(x_values_sorted, y_values_sorted, color=colores[proyecto], label=proyecto if i == 0 else "")
    ax.set_xscale('log')
    ax.set_xlim(0.01, 100)
    ax.xaxis.set_major_locator(LogLocator(base=10, numticks=10))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs='auto', numticks=50))
    def log_format(x, _):
        if x < 1:
            return f"{x:.2f}"
        else:
            return f"{int(x)}"
    ax.xaxis.set_major_formatter(FuncFormatter(log_format))
    ax.invert_xaxis()
    ax.set_xlabel('Tamaño de partícula (mm)')
    ax.set_ylabel('Porcentaje que pasa (%)')
    ax.set_title('Distribución Granulométrica', pad=40)
    handles, labels = ax.get_legend_handles_labels()
    max_legends = 27
    if len(handles) > max_legends:
        handles = handles[:max_legends]
        labels = labels[:max_legends]
    ax.legend(handles, labels, loc='upper right', fontsize=8, ncol=1, columnspacing=0.5,
              handlelength=2, handletextpad=0.5, borderpad=0.5, framealpha=0.5, borderaxespad=0.5)
    ax.axvline(x=76.8, color='black', linestyle='--', linewidth=1, label='3')
    ax.axvline(x=19, color='black', linestyle='--', linewidth=1, label='3/4')
    ax.axvline(x=4.76, color='black', linestyle='--', linewidth=1, label='N°4')
    ax.axvline(x=0.42, color='black', linestyle='--', linewidth=1, label='N°40')
    ax.axvline(x=0.0749, color='black', linestyle='--', linewidth=1, label='N°200')
    ax.axhline(y=50, color='black', linestyle='--', linewidth=1, label='50')
    ax.text(76.8, 106.5, '3', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(19, 106.5, '3/4', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(4.76, 106.5, '4', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(0.42, 106.5, '40', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(0.0749, 106.5, '200', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(140, 50, '50', color='black', va='bottom', ha='left', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    def add_text_with_box(ax, x, y, text, color, pad=0.5, boxstyle='square'):
        ax.text(x, y, text, color=color, va='bottom', ha='center', fontsize=8,
                bbox=dict(facecolor='white', edgecolor="black", boxstyle=boxstyle, pad=pad))
    add_text_with_box(ax, 19, 112, "    G    R    A    V    A     ", color='black', pad=0.3)
    add_text_with_box(ax, 0.60, 112, '      A         R         E         N         A      ', color='black', pad=0.3)
    add_text_with_box(ax, 0.025, 112, '   F   I   N   O   S   ', color='black', pad=0.3)
    plt.grid(True)
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches="tight", pad_inches=0.5)
    buffer.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

#grafico de granulometria por prospeccion
def generar_grafico_granulometria_prospeccion(df):
    df['id_prospeccion'] = df['id_prospeccion'].astype(str)
    df['id_prospeccion_unico'] = df.groupby('id_prospeccion').cumcount() + 1
    df['etiqueta'] = df['id_prospeccion'] + '-' + df['id_prospeccion_unico'].astype(str)
    prospecciones_unicas = df['etiqueta'].unique()
    colores = {prospeccion: np.random.rand(3,) for prospeccion in prospecciones_unicas}
    fig, ax = plt.subplots()
    x_values = np.array([0.075, 0.110, 0.250, 0.420, 0.840, 2.000, 4.760, 9.520, 19.000, 25.400, 38.100, 50.800, 63.500, 75.000])
    for prospeccion in prospecciones_unicas:
        datos_prospeccion = df[df['etiqueta'] == prospeccion]
        y_values = datos_prospeccion.iloc[0, 2:16].values
        sorted_indices = np.argsort(x_values)[::-1]
        x_values_sorted = x_values[sorted_indices]
        y_values_sorted = y_values[sorted_indices]
        ax.plot(x_values_sorted, y_values_sorted, color=colores[prospeccion], label=prospeccion)
    ax.set_xscale('log')
    ax.set_xlim(0.01, 100)
    ax.xaxis.set_major_locator(LogLocator(base=10, numticks=10))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs='auto', numticks=50))
    def log_format(x, _):
        if x < 1:
            return f"{x:.2f}"
        else:
            return f"{int(x)}"
    ax.xaxis.set_major_formatter(FuncFormatter(log_format))
    ax.invert_xaxis()
    ax.set_xlabel('Tamaño de partícula (mm)')
    ax.set_ylabel('Porcentaje que pasa (%)')
    ax.set_title('Distribución Granulométrica por Prospección', pad=40)
    handles, labels = ax.get_legend_handles_labels()
    max_legends = 27
    if len(handles) > max_legends:
        handles = handles[:max_legends]
        labels = labels[:max_legends]
    ax.legend(handles, labels, loc='upper right', fontsize=8, ncol=1, columnspacing=0.5,
              handlelength=2, handletextpad=0.5, borderpad=0.5, framealpha=0.5, borderaxespad=0.5)
    ax.axvline(x=76.8, color='black', linestyle='--', linewidth=1, label='3')
    ax.axvline(x=19, color='black', linestyle='--', linewidth=1, label='3/4')
    ax.axvline(x=4.76, color='black', linestyle='--', linewidth=1, label='N°4')
    ax.axvline(x=0.42, color='black', linestyle='--', linewidth=1, label='N°40')
    ax.axvline(x=0.0749, color='black', linestyle='--', linewidth=1, label='N°200')
    ax.axhline(y=50, color='black', linestyle='--', linewidth=1, label='50')
    ax.text(76.8, 106.5, '3', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(19, 106.5, '3/4', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(4.76, 106.5, '4', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(0.42, 106.5, '40', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(0.0749, 106.5, '200', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(140, 50, '50', color='black', va='bottom', ha='left', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    def add_text_with_box(ax, x, y, text, color, pad=0.5, boxstyle='square'):
        ax.text(x, y, text, color=color, va='bottom', ha='center', fontsize=8,
                bbox=dict(facecolor='white', edgecolor="black", boxstyle=boxstyle, pad=pad))
    add_text_with_box(ax, 19, 112, "    G    R    A    V    A     ", color='black', pad=0.3)
    add_text_with_box(ax, 0.60, 112, '      A         R         E         N         A      ', color='black', pad=0.3)
    add_text_with_box(ax, 0.025, 112, '   F   I   N   O   S   ', color='black', pad=0.3)
    plt.grid(True)
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches="tight", pad_inches=0.5)
    buffer.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

#Funcion graficos granulometria
def graficos_granulometria(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    tipos_prospeccion = request.GET.getlist('tipo_prospeccion')
    areas = request.GET.getlist('area')
    id_prospecciones = request.GET.getlist('id_prospeccion')
    query = Granulometria.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    if id_prospecciones:
        query = query.filter(id_prospeccion__in=id_prospecciones)
    proyectos = query.values('id_proyecto').distinct()
    tipos_prospeccion_inicial = (query.values_list('tipo_prospeccion', flat=True)
                                .distinct().exclude(tipo_prospeccion__isnull=True).exclude(tipo_prospeccion=''))
    areas_inicial = (query.values_list('area', flat=True)
                     .distinct().exclude(area__isnull=True).exclude(area=''))
    id_prospecciones_inicial = (query.values_list('id_prospeccion', flat=True)
                                .distinct().exclude(id_prospeccion__isnull=True).exclude(id_prospeccion=''))
    granulometrias = Granulometria.objects.all()
    if id_proyectos:
        granulometrias = granulometrias.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        granulometrias = granulometrias.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        granulometrias = granulometrias.filter(area__in=areas)
    if id_prospecciones:
        granulometrias = granulometrias.filter(id_prospeccion__in=id_prospecciones)
    df = pd.DataFrame.from_records(granulometrias.values(
        'id_proyecto', 'id_prospeccion', 'n_0075', 'n_0110', 'n_0250', 'n_0420', 'n_0840',
        'n_2000', 'n_4760', 'n_9520', 'n_19000', 'n_25400', 'n_38100', 'n_50800', 'n_63500', 'n_75000', 'area'
    ))
    context = {
        'proyectos': proyectos,
        'tipos_prospeccion_inicial': tipos_prospeccion_inicial,
        'areas_inicial': areas_inicial,
        'id_prospecciones_inicial': id_prospecciones_inicial,
        'selected_id_proyectos': json.dumps(id_proyectos),
        'selected_tipos_prospeccion': json.dumps(tipos_prospeccion),
        'selected_areas': json.dumps(areas),
        'selected_id_prospecciones': json.dumps(id_prospecciones),
    }
    if df.empty:
        context['error'] = "No hay datos para graficar."
        return render(request, 'laboratorio/ensayos/granulometria/graficos_granulometria.html', context)
    image_base64_proyecto = generar_grafico_granulometria_area(df)
    image_base64_prospeccion = generar_grafico_granulometria_prospeccion(df)
    context.update({
        'image_base64_proyecto': image_base64_proyecto,
        'image_base64_prospeccion': image_base64_prospeccion,
    })
    return render(request, 'laboratorio/ensayos/granulometria/graficos_granulometria.html', context)

# Funciones de API para granulometria
def obtener_tipos_prospeccion_granulometria(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    tipos = Granulometria.objects.all()
    if id_proyectos:
        tipos = tipos.filter(id_proyecto__in=id_proyectos)
    tipos_list = list(tipos.values_list('tipo_prospeccion', flat=True)
                     .distinct()
                     .exclude(tipo_prospeccion__isnull=True)
                     .exclude(tipo_prospeccion=''))
    print(f"Tipos para id_proyectos={id_proyectos}: {tipos_list}")
    return JsonResponse({'options': tipos_list}, safe=False)

def obtener_areas_granulometria(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    areas = Granulometria.objects.all()
    if id_proyectos:
        areas = areas.filter(id_proyecto__in=id_proyectos)
    areas_list = list(areas.values_list('area', flat=True)
                     .distinct()
                     .exclude(area__isnull=True)
                     .exclude(area=''))
    print(f"Áreas para id_proyectos={id_proyectos}: {areas_list}")
    return JsonResponse({'options': areas_list}, safe=False)

def obtener_id_prospecciones_granulometria(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    tipos_prospeccion = request.GET.getlist('tipo_prospeccion')
    areas = request.GET.getlist('area')
    query = Granulometria.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    id_prospecciones_list = list(query.values_list('id_prospeccion', flat=True)
                                .distinct()
                                .exclude(id_prospeccion__isnull=True)
                                .exclude(id_prospeccion=''))
    print(f"ID Prospecciones para id_proyectos={id_proyectos}, tipos={tipos_prospeccion}, areas={areas}: {id_prospecciones_list}")
    return JsonResponse({'options': id_prospecciones_list}, safe=False)

def obtener_id_proyecto_granulometria(request):
    tipos_prospeccion = request.GET.getlist('tipo_prospeccion')
    areas = request.GET.getlist('area')
    id_prospecciones = request.GET.getlist('id_prospeccion')
    query = Granulometria.objects.all()
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    if id_prospecciones:
        query = query.filter(id_prospeccion__in=id_prospecciones)
    proyectos_list = list(query.values_list('id_proyecto', flat=True)
                         .distinct()
                         .exclude(id_proyecto__isnull=True)
                         .exclude(id_proyecto=''))
    print(f"Proyectos para tipos={tipos_prospeccion}, areas={areas}, id_prospecciones={id_prospecciones}: {proyectos_list}")
    return JsonResponse({'options': proyectos_list}, safe=False)




#### MUESTREO ##############################################

# Agregar muestreo
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Proyectos, Prospecciones, Muestreo
from .forms import MuestreoForm

logger = logging.getLogger(__name__)

@login_required
def agregar_muestreo(request):
    proyectos = Proyectos.objects.all()
    if request.method == 'POST':
        logger.debug(f"Datos enviados: {request.POST}")
        form = MuestreoForm(request.POST)
        if form.is_valid():
            muestreo = form.save(commit=False)
            muestreo.user = request.user
            # Asignar tipo_prospeccion desde el formulario
            muestreo.tipo_prospeccion = request.POST.get('tipo_prospeccion', '')
            try:
                muestreo.save()
                logger.info(f"Muestreo creado: ID {muestreo.id}")
                return redirect('listar_muestreo')
            except Exception as e:
                logger.error(f"Error al guardar muestreo: {e}")
                return render(request, 'terreno/muestreo/agregar_muestreo.html', {
                    'form': form, 'proyectos': proyectos, 'errors': [str(e)]
                })
        else:
            logger.debug(f"Errores del formulario: {form.errors}")
            return render(request, 'terreno/muestreo/agregar_muestreo.html', {
                'form': form, 'proyectos': proyectos, 'errors': form.errors
            })
    else:
        form = MuestreoForm()
    return render(request, 'terreno/muestreo/agregar_muestreo.html', {
        'form': form, 'proyectos': proyectos
    })  
    
# Listar muestreo
def listar_muestreo(request):
    muestreos = Muestreo.objects.all().order_by('id')  # Cambiar n por id
    query = request.GET.get('q', '')
    if query:
        Muestreo_model = apps.get_model('administrador', 'Muestreo')
        campos = [field.name for field in Muestreo_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        query_filter = Q()
        for field in campos:
            if isinstance(Muestreo_model._meta.get_field(field), (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            elif isinstance(Muestreo_model._meta.get_field(field), ForeignKey):
                related_model = Muestreo_model._meta.get_field(field).related_model
                related_fields = [f"{field}__{related_field.name}" for related_field in related_model._meta.get_fields() if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    query_filter |= Q(**{f"{related_field}__icontains": query})
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        muestreos = muestreos.filter(query_filter)

    paginator = Paginator(muestreos, 1000)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'terreno/muestreo/muestreo_table.html', {'page_obj': page_obj})
    return render(request, 'terreno/muestreo/listar_muestreo.html', {'page_obj': page_obj, 'query': query})

# Exportar a excel
def export_to_excel_muestreo(request):
    muestreo = Muestreo.objects.all().values()
    df = pd.DataFrame(muestreo)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=muestreo.xlsx'
    df.to_excel(response, index=False)
    return response

def export_to_pdf_muestreo(request):
    pass

# Ver muestreo
def ver_muestreo(request, id):  # Cambiar n por id
    muestreo = get_object_or_404(Muestreo, id=id)  # Cambiar pk por id
    return render(request, 'terreno/muestreo/ver_muestreo.html', {'muestreo': muestreo})

# Editar muestreo
@login_required
def editar_muestreo(request, id):  # Cambiar n por id
    muestreo = get_object_or_404(Muestreo, id=id)  # Cambiar pk por id
    form = MuestreoForm(request.POST or None, request.FILES or None, instance=muestreo)
    if request.method == 'POST':
        if form.is_valid():
            muestreo = form.save(commit=False)
            muestreo.user = request.user
            muestreo.save()
            return redirect('listar_muestreo')
        else:
            print('Formulario no es válido')
            print(form.errors)
    return render(request, 'terreno/muestreo/editar_muestreo.html', {'form': form})

# Eliminar muestreo
@login_required
def eliminar_muestreo(request, id):  # Cambiar pk por id
    muestreo = get_object_or_404(Muestreo, id=id)  # Cambiar pk por id
    if request.method == 'POST':
        muestreo.delete()
        return redirect('listar_muestreo')
    return render(request, 'terreno/muestreo/listar_muestreo.html', {'muestreo': muestreo})







############ PROGRAMA ##############################################

@login_required
def agregar_programa(request):
    proyectos = Proyectos.objects.all()
    if request.method == 'POST':
        post_data = request.POST.copy()
        proyecto_id = post_data.get('id_proyecto')
        if proyecto_id:
            try:
                proyecto = Proyectos.objects.get(id=proyecto_id)
                post_data['id_proyecto'] = proyecto
            except Proyectos.DoesNotExist:
                post_data['id_proyecto'] = None
        
        form = ProgramaForm(post_data)
        if form.is_valid():
            try:
                programa = form.save(commit=False)
                programa.user = request.user
                programa.save()
                print(f"Programa creado: ID {programa.id}")  # Depuración
                return redirect('listar_programa')
            except Exception as e:
                print(f"Error al guardar programa: {e}")  # Depuración
                form.add_error(None, f"Error al guardar: {e}")
        else:
            print("Formulario no válido:", form.errors)  # Depuración
    else:
        form = ProgramaForm()
    return render(request, 'laboratorio/programa/agregar_programa.html', {'form': form, 'proyectos': proyectos})

# Listar programas
@login_required
def listar_programa(request):
    programas = Programa.objects.all().order_by('id')
    query = request.GET.get('q', '')
    if query:
        Programa_model = apps.get_model('administrador', 'Programa')
        fields = [field.name for field in Programa_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        query_filter = Q()
        for field in fields:
            if isinstance(Programa_model._meta.get_field(field), (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            elif isinstance(Programa_model._meta.get_field(field), ForeignKey):
                related_model = Programa_model._meta.get_field(field).related_model
                related_fields = [f"{field}__{related_field.name}" for related_field in related_model._meta.get_fields() if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    query_filter |= Q(**{f"{related_field}__icontains": query})
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        programas = programas.filter(query_filter)

    paginator = Paginator(programas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'laboratorio/programa/programa_table.html', {'page_obj': page_obj})
    return render(request, 'laboratorio/programa/listar_programa.html', {'page_obj': page_obj, 'query': query})

# Exportar a Excel
@login_required
def export_to_excel_programa(request):
    query = request.GET.get('q', '')
    headers = [
        'ID', 'ID Proyecto', 'Tipo Prospección', 'ID Prospección', 'Área', 'Objetivo', 'Cantidad', 
        'Fecha Ingreso Lab', 'ID Ingreso', 'Fecha Envío', 'Asignar Muestra', 'Fecha Informe', 
        'Cantidad Recibida', 'N° Informe', 'N° EP', 'Usuario'
    ]

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="programas_filtrados.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Programas Filtrados"
    ws.append(headers)

    programas = Programa.objects.all().order_by('id')
    if query:
        Programa_model = apps.get_model('administrador', 'Programa')
        fields = [field.name for field in Programa_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        query_filter = Q()
        for field in fields:
            if isinstance(Programa_model._meta.get_field(field), (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            elif isinstance(Programa_model._meta.get_field(field), ForeignKey):
                related_model = Programa_model._meta.get_field(field).related_model
                related_fields = [f"{field}__{related_field.name}" for related_field in related_model._meta.get_fields() if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    query_filter |= Q(**{f"{related_field}__icontains": query})
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        programas = programas.filter(query_filter)

    for programa in programas:
        row = [
            programa.id,
            str(programa.id_proyecto.id) if programa.id_proyecto else 'N/A',
            programa.tipo_prospeccion or 'N/A',
            str(programa.id_prospeccion.id) if programa.id_prospeccion else 'N/A',
            programa.area or 'N/A',
            programa.objetivo or 'N/A',
            programa.cantidad or 'N/A',
            programa.fecha_ingreso_lab.strftime('%d/%m/%Y') if programa.fecha_ingreso_lab else 'N/A',
            programa.id_ingreso or 'N/A',
            programa.fecha_envio_programa.strftime('%d/%m/%Y') if programa.fecha_envio_programa else 'N/A',
            programa.asignar_muestra or 'N/A',
            programa.fecha_informe.strftime('%d/%m/%Y') if programa.fecha_informe else 'N/A',
            programa.cantidad_recibida or 'N/A',
            programa.n_informe or 'N/A',
            programa.n_ep or 'N/A',
            programa.user.username if programa.user else 'Sin usuario'
        ]
        ws.append(row)

    wb.save(response)
    return response

# Exportar a PDF
@login_required
def export_to_pdf_programa(request):
    query = request.GET.get('q', '')
    headers = [
        'ID', 'ID Proyecto', 'Tipo Prospección', 'ID Prospección', 'Área', 'Objetivo', 'Cantidad', 
        'Fecha Ingreso Lab', 'ID Ingreso', 'Fecha Envío', 'Asignar Muestra', 'Fecha Informe', 
        'Cantidad Recibida', 'N° Informe', 'N° EP', 'Usuario'
    ]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="programas_filtrados.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Reporte de Programas Filtrados")
    p.drawString(100, 730, " | ".join(headers))

    programas = Programa.objects.all().order_by('id')
    if query:
        Programa_model = apps.get_model('administrador', 'Programa')
        fields = [field.name for field in Programa_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        query_filter = Q()
        for field in fields:
            if isinstance(Programa_model._meta.get_field(field), (DateField, DateTimeField)):
                query_filter |= Q(**{f"{field}__year__icontains": query})
                query_filter |= Q(**{f"{field}__month__icontains": query})
                query_filter |= Q(**{f"{field}__day__icontains": query})
            elif isinstance(Programa_model._meta.get_field(field), ForeignKey):
                related_model = Programa_model._meta.get_field(field).related_model
                related_fields = [f"{field}__{related_field.name}" for related_field in related_model._meta.get_fields() if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    query_filter |= Q(**{f"{related_field}__icontains": query})
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        programas = programas.filter(query_filter)

    y = 710
    for programa in programas:
        row = [
            str(programa.id),
            str(programa.id_proyecto.id) if programa.id_proyecto else 'N/A',
            programa.tipo_prospeccion or 'N/A',
            str(programa.id_prospeccion.id) if programa.id_prospeccion else 'N/A',
            programa.area or 'N/A',
            programa.objetivo or 'N/A',
            str(programa.cantidad) if programa.cantidad else 'N/A',
            programa.fecha_ingreso_lab.strftime('%d/%m/%Y') if programa.fecha_ingreso_lab else 'N/A',
            programa.id_ingreso or 'N/A',
            programa.fecha_envio_programa.strftime('%d/%m/%Y') if programa.fecha_envio_programa else 'N/A',
            programa.asignar_muestra or 'N/A',
            programa.fecha_informe.strftime('%d/%m/%Y') if programa.fecha_informe else 'N/A',
            str(programa.cantidad_recibida) if programa.cantidad_recibida else 'N/A',
            programa.n_informe or 'N/A',
            programa.n_ep or 'N/A',
            programa.user.username if programa.user else 'Sin usuario'
        ]
        text = " | ".join(row)
        p.drawString(100, y, text[:500])  # Limitar longitud para evitar desbordamiento
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    return response

# Ver programa
@login_required
def ver_programa(request, id):
    programa = get_object_or_404(Programa, id=id)
    return render(request, 'laboratorio/programa/ver_programa.html', {'programa': programa})

# Editar programa
@login_required
def editar_programa(request, id):
    programa = get_object_or_404(Programa, id=id)
    proyectos = Proyectos.objects.all()
    if request.method == 'POST':
        form = ProgramaForm(request.POST, instance=programa)
        if form.is_valid():
            form.save()
            return redirect('listar_programa')
    else:
        form = ProgramaForm(instance=programa)
    return render(request, 'laboratorio/programa/editar_programa.html', {
        'form': form,
        'programa': programa,
        'proyectos': proyectos
    })

# Eliminar programa
@login_required
def eliminar_programa(request, id):
    programa = get_object_or_404(Programa, id=id)
    if request.method == 'POST':
        programa.delete()
        return redirect('listar_programa')
    return render(request, 'laboratorio/programa/eliminar_programa.html', {'programa': programa})

# Estatus programa (sin cambios significativos, ya usa id)
@login_required
def estatus_programa(request):
    id_proyecto = request.GET.get('id_proyecto')
    tipo_prospeccion = request.GET.get('tipo_prospeccion')
    objetivo = request.GET.get('objetivo')
    programas = Programa.objects.all()
    if id_proyecto:
        programas = programas.filter(id_proyecto=id_proyecto)
    if tipo_prospeccion:
        programas = programas.filter(tipo_prospeccion=tipo_prospeccion)
    if objetivo:
        programas = programas.filter(objetivo=objetivo)

    df = pd.DataFrame.from_records(programas.values('objetivo', 'cantidad', 'cantidad_recibida'))
    objetivo_counts = df.groupby('objetivo')['cantidad'].sum().sort_index()
    avance_counts = df.groupby('objetivo')['cantidad_recibida'].sum().sort_index()

    if len(objetivo_counts) != len(avance_counts):
        avance_counts = avance_counts.reindex(objetivo_counts.index, fill_value=0)

    objetivo_counts = objetivo_counts.astype(float)
    avance_counts = avance_counts.astype(float)
    total_count = float(objetivo_counts.sum())
    total_avance = float(avance_counts.sum())

    # Gráfico de barras horizontales
    plt.figure(figsize=(12, len(objetivo_counts) * 0.5))
    indices = np.arange(len(objetivo_counts))
    bar_width = 0.35
    plt.barh(indices, objetivo_counts, bar_width, label='Total', color='lightgray')
    plt.barh(indices, avance_counts, bar_width, label='Avance', color='blue')
    plt.xlabel('Conteo')
    plt.ylabel('Objetivo')
    plt.title('Estatus de Programas')
    plt.yticks(indices, objetivo_counts.index)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Mover la leyenda fuera del gráfico
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Etiquetas de valores fuera de las barras
    max_value = objetivo_counts.max()
    for i, (total, avance) in enumerate(zip(objetivo_counts, avance_counts)):
        plt.text(max_value + 0.5, i, f'{avance}', va='center', color='blue')
    
    plt.tight_layout()

    buffer_barras = BytesIO()
    plt.savefig(buffer_barras, format='png')
    buffer_barras.seek(0)
    image_base64_barras = base64.b64encode(buffer_barras.getvalue()).decode('utf-8')
    plt.close()

    # Gráfico de anillo (sin cambios)
    plt.figure(figsize=(4, 4))
    labels = ['Avance', 'Pendiente']
    sizes = [total_avance, total_count - total_avance]
    colors = ['blue', 'lightgray']
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Porcentaje Total de Avance')
    plt.tight_layout()

    buffer_anillo = BytesIO()
    plt.savefig(buffer_anillo, format='png')
    buffer_anillo.seek(0)
    image_base64_anillo = base64.b64encode(buffer_anillo.getvalue()).decode('utf-8')
    plt.close()

    proyectos = Proyectos.objects.all()
    return render(request, 'laboratorio/programa/estatus_programa.html', {
        'image_base64_barras': image_base64_barras,
        'image_base64_anillo': image_base64_anillo,
        'proyectos': proyectos
    })


############ AUDITORIAS ##############################################

# Auditoria prospecciones
def historial(request):
    historiales = Prospecciones.history.all()
    cambios = []
    for historial in historiales:
        if historial.prev_record:
            diff = historial.diff_against(historial.prev_record)
            for change in diff.changes:
                cambios.append({
                    'fecha': historial.history_date,
                    'usuario': historial.history_user,  # Cambiar nomina por usuario
                    'campo': change.field,
                    'valor_anterior': change.old,
                    'valor_nuevo': change.new,
                    'resumen': f"En la fecha {historial.history_date} se modificó el campo {change.field} de {change.old} a {change.new}"
                })
    return render(request, 'historial.html', {'cambios': cambios})







#######NOMINA##########################################################################################
# Configurar logging

logger = logging.getLogger(__name__)

# Agregar nómina
@login_required
def agregar_nomina(request):
    form = NominaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                nomina = form.save(commit=False)
                nomina.user = request.user
                nomina.primer_dia = nomina.primer_dia or nomina.fecha_ingreso or date.today()
                nomina.save()
                logger.info(f"Nómina creada: ID {nomina.id}, Turno: {nomina.turno}")
                nomina.generar_roster_para_nomina()
                return redirect('listar_nomina')
            except Exception as e:
                logger.error(f"Error al guardar nómina: {e}")
                form.add_error(None, f"Error al guardar: {e}")
        else:
            logger.error(f"Formulario no válido: {form.errors}")
            print('Formulario no válido', form.errors)
    return render(request, 'nomina/agregar_nomina.html', {'form': form, 'errors': form.errors})

# Listar nómina
@login_required
def listar_nomina(request):
    nomina_list = Nomina.objects.select_related('id_proyecto').all().order_by('id')
    consulta = request.GET.get('q', '')
    if consulta:
        campos = [field.name for field in Nomina._meta.get_fields() 
                  if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        filtro_consulta = Q()
        for campo in campos:
            if isinstance(Nomina._meta.get_field(campo), (DateField, DateTimeField)):
                filtro_consulta |= Q(**{f"{campo}__year__icontains": consulta})
                filtro_consulta |= Q(**{f"{campo}__month__icontains": consulta})
                filtro_consulta |= Q(**{f"{campo}__day__icontains": consulta})
            elif isinstance(Nomina._meta.get_field(campo), ForeignKey):
                related_model = Nomina._meta.get_field(campo).related_model
                related_fields = [f"{campo}__{related_field.name}" for related_field in related_model._meta.get_fields() 
                                  if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    filtro_consulta |= Q(**{f"{related_field}__icontains": consulta})
            else:
                filtro_consulta |= Q(**{f"{campo}__icontains": consulta})
        nomina_list = nomina_list.filter(filtro_consulta)

    paginator = Paginator(nomina_list, 1000)  # 10 registros por página
    page_number = request.GET.get('page')
    nomina_list = paginator.get_page(page_number)
    return render(request, 'nomina/listar_nomina.html', {'nomina_list': nomina_list, 'consulta': consulta})

from django.http import HttpResponse
from openpyxl import Workbook
def export_to_excel_nomina(request):
    query = request.GET.get('q', '')
    headers_str = request.GET.get('headers', '')
    headers = headers_str.split(',') if headers_str else [
        'ID', 'Proyecto', 'Empresa', 'Fecha Ingreso', 'Nombre', 'Apellido', 'RUT', 'Email',
        'Teléfono', 'Cargo', 'Título', 'Turno', 'Horas Semanales', 'Primer Día'
    ]

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="nomina_filtrada.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Nómina Filtrada"
    ws.append(headers)

    nominas = Nomina.objects.select_related('id_proyecto').all().order_by('id')
    if query:
        campos = [field.name for field in Nomina._meta.get_fields() 
                  if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        filtro_consulta = Q()
        for campo in campos:
            if isinstance(Nomina._meta.get_field(campo), (DateField, DateTimeField)):
                filtro_consulta |= Q(**{f"{campo}__year__icontains": query})
                filtro_consulta |= Q(**{f"{campo}__month__icontains": query})
                filtro_consulta |= Q(**{f"{campo}__day__icontains": query})
            elif isinstance(Nomina._meta.get_field(campo), ForeignKey):
                related_model = Nomina._meta.get_field(campo).related_model
                related_fields = [f"{campo}__{related_field.name}" for related_field in related_model._meta.get_fields() 
                                  if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    filtro_consulta |= Q(**{f"{related_field}__icontains": query})
            else:
                filtro_consulta |= Q(**{f"{campo}__icontains": query})
        nominas = nominas.filter(filtro_consulta)

    for nomina in nominas:
        row = []
        for header in headers:
            if header == 'ID':
                value = nomina.id
            elif header == 'Proyecto':
                value = str(nomina.id_proyecto) if nomina.id_proyecto else 'N/A'
            elif header == 'Empresa':
                value = nomina.empresa
            elif header == 'Fecha Ingreso':
                value = nomina.fecha_ingreso.strftime('%d/%m/%Y') if nomina.fecha_ingreso else 'N/A'
            elif header == 'Nombre':
                value = nomina.nombre
            elif header == 'Apellido':
                value = nomina.apellido
            elif header == 'RUT':
                value = nomina.rut
            elif header == 'Email':
                value = nomina.email
            elif header == 'Teléfono':
                value = nomina.telefono
            elif header == 'Cargo':
                value = nomina.cargo
            elif header == 'Título':
                value = nomina.titulo
            elif header == 'Turno':
                value = nomina.turno if nomina.turno else 'N/A'
            elif header == 'Horas Semanales':
                value = float(nomina.horas_semanales) if nomina.horas_semanales is not None else 'N/A'
            elif header == 'Primer Día':
                value = nomina.primer_dia.strftime('%d/%m/%Y') if nomina.primer_dia else 'N/A'
            else:
                value = 'N/A'
            row.append(value)
        ws.append(row)

    wb.save(response)
    return response



@login_required
def export_to_pdf_nomina(request):
    query = request.GET.get('q', '')
    headers_str = request.GET.get('headers', '')
    headers = headers_str.split(',') if headers_str else [
        'ID', 'Proyecto', 'Empresa', 'Fecha Ingreso', 'Nombre', 'Apellido', 'RUT', 'Email',
        'Teléfono', 'Cargo', 'Título', 'Turno', 'Horas Semanales', 'Primer Día'
    ]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="nomina_filtrada.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Reporte de Nómina Filtrada")
    p.drawString(100, 730, " | ".join(headers))

    nominas = Nomina.objects.select_related('id_proyecto').all().order_by('id')
    if query:
        campos = [field.name for field in Nomina._meta.get_fields() 
                  if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        filtro_consulta = Q()
        for campo in campos:
            if isinstance(Nomina._meta.get_field(campo), (DateField, DateTimeField)):
                filtro_consulta |= Q(**{f"{campo}__year__icontains": query})
                filtro_consulta |= Q(**{f"{campo}__month__icontains": query})
                filtro_consulta |= Q(**{f"{campo}__day__icontains": query})
            elif isinstance(Nomina._meta.get_field(campo), ForeignKey):
                related_model = Nomina._meta.get_field(campo).related_model
                related_fields = [f"{campo}__{related_field.name}" for related_field in related_model._meta.get_fields() 
                                  if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    filtro_consulta |= Q(**{f"{related_field}__icontains": query})
            else:
                filtro_consulta |= Q(**{f"{campo}__icontains": query})
        nominas = nominas.filter(filtro_consulta)

    y = 710
    for nomina in nominas:
        row = []
        for header in headers:
            if header == 'ID':
                value = str(nomina.id)
            elif header == 'Proyecto':
                value = str(nomina.id_proyecto) if nomina.id_proyecto else 'N/A'
            elif header == 'Empresa':
                value = nomina.empresa
            elif header == 'Fecha Ingreso':
                value = nomina.fecha_ingreso.strftime('%d/%m/%Y') if nomina.fecha_ingreso else 'N/A'
            elif header == 'Nombre':
                value = nomina.nombre
            elif header == 'Apellido':
                value = nomina.apellido
            elif header == 'RUT':
                value = nomina.rut
            elif header == 'Email':
                value = nomina.email
            elif header == 'Teléfono':
                value = nomina.telefono
            elif header == 'Cargo':
                value = nomina.cargo
            elif header == 'Título':
                value = nomina.titulo
            elif header == 'Turno':
                value = nomina.turno if nomina.turno else 'N/A'
            elif header == 'Horas Semanales':
                value = str(nomina.horas_semanales) if nomina.horas_semanales is not None else 'N/A'
            elif header == 'Primer Día':
                value = nomina.primer_dia.strftime('%d/%m/%Y') if nomina.primer_dia else 'N/A'
            else:
                value = 'N/A'
            row.append(value)
        text = " | ".join(row)
        p.drawString(100, y, text[:500])  # Limitar longitud para evitar desbordamiento
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    return response

# Editar nómina
@login_required
def editar_nomina(request, id):
    nomina = get_object_or_404(Nomina, id=id, user=request.user)
    proyectos = Proyectos.objects.all()
    if request.method == 'POST':
        form = NominaForm(request.POST, instance=nomina)
        if form.is_valid():
            try:
                nomina = form.save()
                logger.info(f"Nómina editada: ID {nomina.id}, Turno: {nomina.turno}")
                nomina.generar_roster_para_nomina()
                return redirect('listar_nomina')
            except Exception as e:
                logger.error(f"Error al editar nómina {nomina.id}: {e}")
                form.add_error(None, f"Error al editar: {e}")
        else:
            logger.error(f"Formulario no válido al editar nómina {nomina.id}: {form.errors}")
    else:
        form = NominaForm(instance=nomina)
    return render(request, 'nomina/editar_nomina.html', {'form': form, 'nomina': nomina, 'proyectos': proyectos})

# Ver nómina
@login_required
def ver_nomina(request, id):
    nomina = get_object_or_404(Nomina, id=id)
    return render(request, 'nomina/ver_nomina.html', {'nomina': nomina})

# Eliminar nómina
@login_required
def eliminar_nomina(request, id):
    nomina = get_object_or_404(Nomina, id=id, user=request.user)
    if request.method == 'POST':
        try:
            nomina.delete()
            logger.info(f"Nómina eliminada: ID {id}")
            return redirect('listar_nomina')
        except Exception as e:
            logger.error(f"Error al eliminar nómina {id}: {e}")
            return HttpResponse(f"Error al eliminar: {e}", status=500)
    return render(request, 'nomina/eliminar_nomina.html', {'nomina': nomina})




###Listar Roster
@login_required
def listar_roster(request):
    # Obtener consulta de búsqueda si existe
    consulta = request.GET.get('q', '')
    
    roster_list = Roster.objects.select_related('nomina__id_proyecto').all()
    nominas = Nomina.objects.select_related('id_proyecto').all()
    
    # Aplicar filtro dinámico si hay consulta
    if consulta:
        # Crear filtro dinámico para Nomina
        campos_nomina = [field.name for field in Nomina._meta.get_fields() 
                        if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        filtro_nomina = Q()
        for campo in campos_nomina:
            if isinstance(Nomina._meta.get_field(campo), (DateField, DateTimeField)):
                filtro_nomina |= Q(**{f"{campo}__year__icontains": consulta})
                filtro_nomina |= Q(**{f"{campo}__month__icontains": consulta})
                filtro_nomina |= Q(**{f"{campo}__day__icontains": consulta})
            elif isinstance(Nomina._meta.get_field(campo), ForeignKey):
                related_model = Nomina._meta.get_field(campo).related_model
                related_fields = [f"{campo}__{related_field.name}" for related_field in related_model._meta.get_fields() 
                                if isinstance(related_field, (CharField, TextField))]
                for related_field in related_fields:
                    filtro_nomina |= Q(**{f"{related_field}__icontains": consulta})
            else:
                filtro_nomina |= Q(**{f"{campo}__icontains": consulta})
        
        # Filtrar las nóminas primero
        nominas = nominas.filter(filtro_nomina)
        
        # Crear filtro dinámico para Roster
        campos_roster = [field.name for field in Roster._meta.get_fields() 
                        if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
        filtro_roster = Q()
        for campo in campos_roster:
            if isinstance(Roster._meta.get_field(campo), (DateField, DateTimeField)):
                filtro_roster |= Q(**{f"{campo}__year__icontains": consulta})
                filtro_roster |= Q(**{f"{campo}__month__icontains": consulta})
                filtro_roster |= Q(**{f"{campo}__day__icontains": consulta})
            elif isinstance(Roster._meta.get_field(campo), ForeignKey):
                filtro_roster |= Q(**{f"{campo}__id__icontains": consulta})
            else:
                filtro_roster |= Q(**{f"{campo}__icontains": consulta})
        
        # Combinar filtros: buscar en Roster y también en las nóminas filtradas
        roster_list = roster_list.filter(filtro_roster | Q(nomina__in=nominas))

    fechas_unicas = roster_list.values_list('fecha', flat=True).distinct().order_by('fecha')
    dias_semana = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}
    dias_del_año = [
        f"{dias_semana[fecha.weekday()]}-{fecha.strftime('%d-%m-%y')}"
        for fecha in fechas_unicas
    ]
    fechas_unicas_str = [fecha.strftime('%Y-%m-%d') for fecha in fechas_unicas]
    
    sumatoria_dias = [
        roster_list.filter(fecha=fecha).aggregate(Sum('horas_asignadas'))['horas_asignadas__sum'] or 0
        for fecha in fechas_unicas
    ]
    
    for nomina in nominas:
        horas_por_dia = []
        roster_nomina = roster_list.filter(nomina=nomina)
        for fecha in fechas_unicas:
            registro = roster_nomina.filter(fecha=fecha).first()
            horas_por_dia.append(float(registro.horas_asignadas) if registro else 0.0)
        nomina.horas_por_dia_lista = horas_por_dia

    # Obtener meses únicos desde los registros de Roster
    meses_unicos = roster_list.values_list('fecha__year', 'fecha__month').distinct().order_by('fecha__year', 'fecha__month')
    resumen_meses = []

    for año, mes in meses_unicos:
        horas_legales = Decimal('0.0')
        horas_totales = Decimal('0.0')
        horas_efectivas = Decimal('0.0')

        for nomina in nominas:
            jornada_teorica = nomina.get_jornada_teorica()
            if jornada_teorica:
                roster_nomina_mes = roster_list.filter(nomina=nomina, fecha__month=mes, fecha__year=año)
                for registro in roster_nomina_mes:
                    horas_asignadas = Decimal(registro.horas_asignadas)
                    if nomina.turno == '5x2 ordinaria':
                        weekday = registro.fecha.weekday()
                        if weekday < 4:  # Lunes a Jueves
                            legal = Decimal('8.5')
                            total = Decimal('9.0')
                        elif weekday == 4:  # Viernes
                            legal = Decimal('6.0')
                            total = Decimal('6.0')
                        else:
                            legal = total = Decimal('0.0')
                    elif nomina.turno == '4x3 excepcional':
                        if horas_asignadas > 0:
                            legal = Decimal('10.0')
                            total = Decimal('11.0')
                        else:
                            legal = total = Decimal('0.0')
                    else:
                        if horas_asignadas > 0:
                            legal = Decimal(jornada_teorica.horas_legales_diarias)
                            total = Decimal(jornada_teorica.horas_totales_diarias)
                        else:
                            legal = total = Decimal('0.0')
                    horas_legales += legal
                    horas_totales += total
                    horas_efectivas += horas_asignadas

        resumen_meses.append({
            'mes': datetime(año, mes, 1),
            'horas_legales': float(horas_legales),
            'horas_efectivas': float(horas_efectivas),
            'horas_totales': float(horas_totales)
        })

    context = {
        'nominas': nominas,
        'dias_del_año': dias_del_año,
        'fechas_unicas': fechas_unicas_str,
        'sumatoria_dias': sumatoria_dias,
        'resumen_meses': resumen_meses,
        'consulta': consulta,
    }
    return render(request, 'nomina/listar_roster.html', context)


# Actualizar horas en el roster
@csrf_exempt
@login_required
def actualizar_hora(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            updated = []
            totals = {}
            for item in data:
                nomina = Nomina.objects.get(id=item['id'], user=request.user)
                roster = Roster.objects.get(nomina=nomina, fecha=item['dia'])
                horas = Decimal(item['valor'])
                if horas < 0 or horas > 24:
                    raise ValueError("Las horas deben estar entre 0 y 24")
                roster.horas_asignadas = horas
                roster.save()
                logger.info(f"Horas actualizadas para roster de nómina {nomina.id}, fecha {item['dia']}: {horas}")
                
                total_horas = Roster.objects.filter(nomina=nomina).aggregate(Sum('horas_asignadas'))['horas_asignadas__sum'] or 0
                nomina.total_horas = total_horas
                nomina.save()
                
                updated.append({
                    'id': nomina.id,
                    'total_trabajador': float(total_horas)
                })
                
                sumatoria_dia = Roster.objects.filter(fecha=item['dia']).aggregate(Sum('horas_asignadas'))['horas_asignadas__sum'] or 0
                totals[item['dia']] = float(sumatoria_dia)
            
            return JsonResponse({
                'success': True,
                'updated': updated,
                'totals': totals
            })
        except (Nomina.DoesNotExist, Roster.DoesNotExist):
            logger.error(f"Registro no encontrado para actualizar hora: {request.body}")
            return JsonResponse({'success': False, 'error': 'Registro no encontrado'}, status=404)
        except ValueError as e:
            logger.error(f"Error de validación al actualizar hora: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error inesperado al actualizar hora: {e}")
            return JsonResponse({'success': False, 'error': f"Error inesperado: {e}"}, status=500)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)




#exportar excel
logger = logging.getLogger(__name__)

@login_required
def export_to_excel_roster(request):
    try:
        consulta = request.GET.get('q', '')
        wb = Workbook()
        ws = wb.active
        ws.title = "Roster"

        # Filtrar datos como en listar_roster
        roster_list = Roster.objects.select_related('nomina__id_proyecto').all()
        nominas = Nomina.objects.select_related('id_proyecto').all()
        
        if consulta:
            campos_nomina = [field.name for field in Nomina._meta.get_fields() 
                            if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
            filtro_nomina = Q()
            for campo in campos_nomina:
                if isinstance(Nomina._meta.get_field(campo), (DateField, DateTimeField)):
                    filtro_nomina |= Q(**{f"{campo}__year__icontains": consulta})
                    filtro_nomina |= Q(**{f"{campo}__month__icontains": consulta})
                    filtro_nomina |= Q(**{f"{campo}__day__icontains": consulta})
                elif isinstance(Nomina._meta.get_field(campo), ForeignKey):
                    related_model = Nomina._meta.get_field(campo).related_model
                    related_fields = [f"{campo}__{related_field.name}" for related_field in related_model._meta.get_fields() 
                                      if isinstance(related_field, (CharField, TextField))]
                    for related_field in related_fields:
                        filtro_nomina |= Q(**{f"{related_field}__icontains": consulta})
                else:
                    filtro_nomina |= Q(**{f"{campo}__icontains": consulta})
            nominas = nominas.filter(filtro_nomina)
            roster_list = roster_list.filter(Q(nomina__in=nominas))

        # Obtener fechas únicas y calcular horas como en listar_roster
        fechas_unicas = roster_list.values_list('fecha', flat=True).distinct().order_by('fecha')
        dias_semana = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
        dias_del_año = [f"{dias_semana[fecha.weekday()]}-{fecha.strftime('%d-%m-%y')}" for fecha in fechas_unicas]
        headers = ["Proyecto", "Nombre", "RUT", "Cargo", "Turno"] + dias_del_año + ["Total Trabajador"]
        ws.append(headers)

        # Calcular horas por día y totales
        for nomina in nominas:
            roster_nomina = roster_list.filter(nomina=nomina)
            roster_dict = {roster.fecha: float(roster.horas_asignadas) for roster in roster_nomina}
            horas_por_dia = [roster_dict.get(fecha, 0.0) for fecha in fechas_unicas]
            nomina.horas_por_dia_lista = horas_por_dia  # Asignar para consistencia

        totales_por_dia = [0.0] * len(fechas_unicas)
        for nomina in nominas:
            row = [
                str(nomina.id_proyecto) if nomina.id_proyecto else "Sin Proyecto",
                f"{nomina.nombre} {nomina.apellido}",
                nomina.rut,
                nomina.cargo,
                nomina.turno if nomina.turno else "N/A"
            ]
            total_trabajador = 0.0
            for i, horas in enumerate(nomina.horas_por_dia_lista):
                row.append(horas)
                total_trabajador += horas
                totales_por_dia[i] += horas
            row.append(total_trabajador)
            ws.append(row)

        total_row = ["Total por Día", "", "", "", ""] + totales_por_dia + [""]
        ws.append(total_row)

        # Ajustar ancho de columnas
        for col in ws.columns:
            max_length = max(len(str(cell.value)) for cell in col if cell.value)
            column = col[0].column_letter
            ws.column_dimensions[column].width = min(max_length + 2, 15)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="roster.xlsx"'
        wb.save(response)
        return response
    except Exception as e:
        logger.error(f"Error al generar archivo Excel: {str(e)}")
        return HttpResponse(f"Error al generar el archivo Excel: {str(e)}", status=500)
    



#Exportar pdf
logger = logging.getLogger(__name__)

@login_required
def export_to_pdf_roster(request):
    try:
        consulta = request.GET.get('q', '')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="roster.pdf"'
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Filtrar datos como en listar_roster
        roster_list = Roster.objects.select_related('nomina__id_proyecto').all()
        nominas = Nomina.objects.select_related('id_proyecto').all()
        
        if consulta:
            campos_nomina = [field.name for field in Nomina._meta.get_fields() 
                            if isinstance(field, (CharField, TextField, DateField, DateTimeField, ForeignKey))]
            filtro_nomina = Q()
            for campo in campos_nomina:
                if isinstance(Nomina._meta.get_field(campo), (DateField, DateTimeField)):
                    filtro_nomina |= Q(**{f"{campo}__year__icontains": consulta})
                    filtro_nomina |= Q(**{f"{campo}__month__icontains": consulta})
                    filtro_nomina |= Q(**{f"{campo}__day__icontains": consulta})
                elif isinstance(Nomina._meta.get_field(campo), ForeignKey):
                    related_model = Nomina._meta.get_field(campo).related_model
                    related_fields = [f"{campo}__{related_field.name}" for related_field in related_model._meta.get_fields() 
                                      if isinstance(related_field, (CharField, TextField))]
                    for related_field in related_fields:
                        filtro_nomina |= Q(**{f"{related_field}__icontains": consulta})
                else:
                    filtro_nomina |= Q(**{f"{campo}__icontains": consulta})
            nominas = nominas.filter(filtro_nomina)
            roster_list = roster_list.filter(Q(nomina__in=nominas))

        # Obtener fechas únicas y calcular horas como en listar_roster
        fechas_unicas = roster_list.values_list('fecha', flat=True).distinct().order_by('fecha')
        dias_semana = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
        dias_del_año = [f"{dias_semana[fecha.weekday()]}-{fecha.strftime('%d-%m-%y')}" for fecha in fechas_unicas]
        headers = ["Proyecto", "Nombre", "RUT", "Cargo", "Turno"] + dias_del_año + ["Total Trabajador"]
        data = [headers]

        # Calcular horas por día y totales
        for nomina in nominas:
            roster_nomina = roster_list.filter(nomina=nomina)
            roster_dict = {roster.fecha: float(roster.horas_asignadas) for roster in roster_nomina}
            horas_por_dia = [roster_dict.get(fecha, 0.0) for fecha in fechas_unicas]
            nomina.horas_por_dia_lista = horas_por_dia  # Asignar para consistencia

        totales_por_dia = [0.0] * len(fechas_unicas)
        for nomina in nominas:
            row = [
                str(nomina.id_proyecto) if nomina.id_proyecto else "Sin Proyecto",
                f"{nomina.nombre} {nomina.apellido}",
                nomina.rut,
                nomina.cargo,
                nomina.turno if nomina.turno else "N/A"
            ]
            total_trabajador = 0.0
            for i, horas in enumerate(nomina.horas_por_dia_lista):
                row.append(str(horas))
                total_trabajador += horas
                totales_por_dia[i] += horas
            row.append(str(total_trabajador))
            data.append(row)

        total_row = ["Total por Día", "", "", "", ""] + [str(total) for total in totales_por_dia] + [""]
        data.append(total_row)

        # Crear la tabla
        table = Table(data, colWidths=[80, 120, 80, 60, 80] + [40] * (len(fechas_unicas) + 1))
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
        ]))
        elements.append(table)

        doc.build(elements)
        return response
    except Exception as e:
        logger.error(f"Error al generar archivo PDF: {str(e)}")
        return HttpResponse(f"Error al generar el archivo PDF: {str(e)}", status=500)
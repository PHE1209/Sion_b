from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, F, CharField, TextField, DateField, DateTimeField, ForeignKey, Sum
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.apps import apps
from datetime import datetime, date, timedelta
from decimal import Decimal
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import csv
from openpyxl import Workbook
from matplotlib.ticker import LogLocator, FuncFormatter, MaxNLocator
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from django.forms.models import model_to_dict
from .models import Nomina, Roster, Proyectos
from .forms import NominaForm
from django.shortcuts import render
from django.http import JsonResponse
from .models import Granulometria
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
import json
from matplotlib.ticker import LogLocator, FuncFormatter
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter
from io import BytesIO
import base64
from django.http import JsonResponse
from django.shortcuts import render
from .models import Granulometria  # Asegúrate de importar tu modelo correctamente




# Importación de modelos
from .models import (Nomina, Proyectos, Prospecciones, Humedad, Area, Muestreo, Programa, Granulometria, Roster, JornadaTeorica, Nomina)

# Importación de formularios
from .forms import (LoginForm, ProyectoEditForm, ProspeccionesForm, HumedadForm, MuestreoForm, GranulometriaForm, ProgramaForm, NominaForm)




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
            proyecto.user = request.user  # Captura el usuario que realiza la operación
            proyecto.save()
            return redirect('listar_proyectos')
    else:
        form = ProyectoEditForm()
    return render(request, 'proyectos/agregar_proyectos.html', {'form': form})

# Listar proyecto
def listar_proyectos(request):
    proyectos = Proyectos.objects.all().order_by('id')  # Ordenar por id
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
def ver_proyectos(request, id):  # Cambiar n por id
    proyecto = get_object_or_404(Proyectos, id=id)  # Cambiar pk por id
    return render(request, 'ver_proyectos.html', {'proyecto': proyecto})

# Eliminar proyecto
def eliminar_proyectos(request, id):  # Cambiar n por id
    proyecto = get_object_or_404(Proyectos, id=id)  # Cambiar pk por id
    if request.method == 'POST':
        proyecto.delete()
        return redirect('listar_proyectos')
    return render(request, 'eliminar_proyectos.html', {'proyecto': proyecto})

def grafico(request):
    texto = "¡Hola! Esta es una vista de texto simple."
    return render(request, 'grafico.html', {'grafico': grafico})

# Editar proyecto
def editar_proyectos(request, id):  # Cambiar n por id
    proyecto = get_object_or_404(Proyectos, id=id)  # Cambiar n por id
    if request.method == 'POST':
        proyecto.pm = request.POST.get('pm')
        proyecto.empresa = request.POST.get('empresa')
        proyecto.nombre = request.POST.get('nombre')
        proyecto.alcance = request.POST.get('alcance')
        proyecto.fecha_inicio = request.POST.get('fecha_inicio')
        proyecto.fecha_termino = request.POST.get('fecha_termino')
        proyecto.save()
        return redirect('listar_proyectos')
    return render(request, 'proyectos/editar_proyectos.html', {'proyecto': proyecto})

# Exportar a excel
def export_to_excel_proyectos(request):
    proyectos = Proyectos.objects.all().values()
    df = pd.DataFrame(proyectos)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=proyectos.xlsx'
    df.to_excel(response, index=False)
    return response

def export_to_pdf_proyectos(request):
    pass




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


##################################

# Obtener tipos de prospección
def obtener_tipos_prospeccion(request):
    id_proyecto = request.GET.get('id_proyecto')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto).values('tipo_prospeccion').distinct()
    tipos_prospeccion = {pros['tipo_prospeccion']: pros['tipo_prospeccion'] for pros in prospecciones}
    return JsonResponse(tipos_prospeccion)

# Obtener IDs de prospección
def obtener_id_prospecciones(request):
    id_proyecto = request.GET.get('id_proyecto')
    tipo_prospeccion = request.GET.get('tipo_prospeccion')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto, tipo_prospeccion=tipo_prospeccion).values('id_prospeccion')  # Cambiar n por id_prospeccion
    id_prospecciones = {pros['id_prospeccion']: pros['id_prospeccion'] for pros in prospecciones}  # Cambiar n por id_prospeccion
    return JsonResponse(id_prospecciones)

# Obtener área de prospección
def get_area(request):
    prospeccion_id = request.GET.get('prospeccion_id')
    try:
        prospeccion = Prospecciones.objects.get(id_prospeccion=prospeccion_id)  # Cambiar n por id_prospeccion
        area = prospeccion.area
    except Prospecciones.DoesNotExist:
        area = ''
    return JsonResponse({'area': area})


def obtener_tipos_prospeccion(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    if id_proyectos:
        tipos = Granulometria.objects.filter(id_proyecto__in=id_proyectos).values('tipo_prospeccion').distinct()
    else:
        tipos = Granulometria.objects.values('tipo_prospeccion').distinct()
    tipos_list = [tipo['tipo_prospeccion'] for tipo in tipos if tipo['tipo_prospeccion'] is not None]
    tipos_dict = {tipo: tipo for tipo in tipos_list}
    return JsonResponse(tipos_dict, safe=False)

def obtener_areas_prospecciones(request):
    id_proyectos = request.GET.getlist('id_proyecto')
    if id_proyectos:
        areas = Granulometria.objects.filter(id_proyecto__in=id_proyectos).values('area').distinct()
    else:
        areas = Granulometria.objects.values('area').distinct()
    areas_list = [area['area'] for area in areas if area['area'] is not None]
    areas_dict = {area: area for area in areas_list}
    return JsonResponse(areas_dict, safe=False)

def obtener_id_prospecciones(request):
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
    id_prospecciones = query.values('id_prospeccion').distinct()
    id_prospecciones_list = [id_pros['id_prospeccion'] for id_pros in id_prospecciones if id_pros['id_prospeccion'] is not None]
    id_prospecciones_dict = {id_pros: id_pros for id_pros in id_prospecciones_list}
    return JsonResponse(id_prospecciones_dict, safe=False)

def obtener_proyectos_prospecciones(request, as_json=False):
    proyectos = Granulometria.objects.values('id_proyecto').distinct()
    proyectos_list = [proj['id_proyecto'] for proj in proyectos if proj['id_proyecto'] is not None]
    proyectos_dict = {proj: proj for proj in proyectos_list}
    if as_json:
        return JsonResponse(proyectos_dict, safe=False)
    return proyectos_list





############ ENSAYOS LABORATORIO ##############################################

#### HUMEDAD ##############################################



# Obtener proyectos desde Humedad
def obtener_proyectos_humedad(request):
    humedades = Humedad.objects.values('id_proyecto').distinct()
    proyectos_list = [proj['id_proyecto'] for proj in humedades if proj['id_proyecto']]
    proyectos_dict = {proj: proj for proj in proyectos_list}
    return JsonResponse(proyectos_dict, safe=False)

# Obtener tipos de prospección desde Humedad
def obtener_tipos_prospeccion_humedad(request):
    id_proyecto = request.GET.get('id_proyecto')
    if id_proyecto:
        humedades = Humedad.objects.filter(id_proyecto=id_proyecto).values('tipo_prospeccion').distinct()
        tipos_prospeccion = {hum['tipo_prospeccion']: hum['tipo_prospeccion'] for hum in humedades}
        return JsonResponse(tipos_prospeccion)
    return JsonResponse({})

# Obtener id_prospecciones desde Humedad
def obtener_id_prospecciones_humedad(request):
    id_proyecto = request.GET.get('id_proyecto')
    tipo_prospeccion = request.GET.get('tipo_prospeccion')
    humedades = Humedad.objects.filter(id_proyecto=id_proyecto, tipo_prospeccion=tipo_prospeccion).values('id_prospeccion')  # Cambiar n por id_prospeccion
    id_prospecciones = {pros['id_prospeccion']: pros['id_prospeccion'] for pros in humedades}  # Cambiar n por id_prospeccion
    return JsonResponse(id_prospecciones)


# Obtener áreas desde Humedad
def obtener_areas_humedad(request):
    id_proyecto = request.GET.get('id_proyecto')
    if id_proyecto:
        humedades = Humedad.objects.filter(id_proyecto=id_proyecto).values('area').distinct()
        areas = [hum['area'] for hum in humedades if hum['area']]
        areas_dict = {area: area for area in areas}
        return JsonResponse(areas_dict)
    return JsonResponse({})

# Obtener área desde Prospecciones
def get_area(request):
    prospeccion_id = request.GET.get('prospeccion_id')
    try:
        prospeccion = Prospecciones.objects.get(id_prospeccion=prospeccion_id)  # Cambiar n por id_prospeccion
        area = prospeccion.area
    except Prospecciones.DoesNotExist:
        area = ''
    return JsonResponse({'area': area})

# Agregar humedad
@login_required
def agregar_humedad(request):
    proyectos = obtener_proyectos_prospecciones(request)
    if request.method == 'POST':
        post_data = request.POST.copy()
        proyecto_id = post_data.get('id_proyecto')
        if proyecto_id:
            try:
                proyecto = Proyectos.objects.get(id=proyecto_id)
                post_data['id_proyecto'] = proyecto
                print(f"Proyecto asignado: {proyecto}")
            except Proyectos.DoesNotExist:
                post_data['id_proyecto'] = None
                print("Proyecto no encontrado")
        prospeccion_id = post_data.get('id_prospeccion')
        if prospeccion_id:
            try:
                prospeccion = Prospecciones.objects.get(id_prospeccion=prospeccion_id)  # Cambiar n por id_prospeccion
                post_data['id_prospeccion'] = prospeccion
                print(f"Prospección asignada: {prospeccion}")
            except Prospecciones.DoesNotExist:
                post_data['id_prospeccion'] = None
                print("Prospección no encontrada")
        form = HumedadForm(post_data)
        if form.is_valid():
            humedad = form.save(commit=False)
            humedad.user = request.user
            humedad.save()
            print("Formulario válido. Datos a guardar:", form.cleaned_data)
            return redirect('listar_humedad')
        else:
            print("Formulario no válido. Errores:", form.errors)
    else:
        form = HumedadForm()
    return render(request, 'laboratorio/ensayos/humedad/agregar_humedad.html', {'form': form, 'proyectos': proyectos})

# Listar humedad
def listar_humedad(request):
    humedades = Humedad.objects.all().order_by('id')  # Cambiar n por id
    query = request.GET.get('q', '')
    if query:
        humedades = humedades.filter(
            Q(id_proyecto__id__icontains=query) |
            Q(id_prospeccion__id_prospeccion__icontains=query) |  # Cambiar id_prospeccion por id_prospeccion
            Q(tipo_prospeccion__icontains=query) |
            Q(humedad__icontains=query) |
            Q(profundidad_promedio__icontains=query) |
            Q(area__icontains=query)
        )

    paginator = Paginator(humedades, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'laboratorio/ensayos/humedad/humedad_table.html', {'page_obj': page_obj})
    return render(request, 'laboratorio/ensayos/humedad/listar_humedad.html', {'page_obj': page_obj, 'query': query})

# Exportar a excel
def export_to_excel_humedad(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="humedad.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Humedad Data"
    headers = ['ID', 'Tipo prospeccion', 'ID Proyecto', 'ID Prospección', 'Humedad', 'Profundidad Promedio', 'area']  # Cambiar N por ID
    ws.append(headers)
    humedades = Humedad.objects.all()
    for humedad in humedades:
        id_proyecto = str(humedad.id_proyecto)
        id_prospeccion = str(humedad.id_prospeccion)
        ws.append([humedad.id, humedad.tipo_prospeccion, id_proyecto, id_prospeccion, humedad.humedad, humedad.profundidad_promedio, humedad.area])  # Cambiar n por id
    wb.save(response)
    return response

def export_to_pdf_humedad(request):
    return HttpResponse("Exportar a PDF no está implementado")

# Ver humedad
def ver_humedad(request, id):  # Cambiar pk por id
    humedad = get_object_or_404(Humedad, id=id)  # Cambiar pk por id
    return render(request, 'laboratorio/ensayos/humedad/ver_humedad.html', {'humedad': humedad})

# Editar humedad
def editar_humedad(request, id):  # Cambiar pk por id
    humedad = get_object_or_404(Humedad, id=id)  # Cambiar pk por id
    if request.method == 'POST':
        form = HumedadForm(request.POST, instance=humedad)
        if form.is_valid():
            form.save()
            return redirect('listar_humedad')
    else:
        form = HumedadForm(instance=humedad)
    return render(request, 'laboratorio/ensayos/humedad/editar_humedad.html', {'form': form})

# Eliminar humedad
def eliminar_humedad(request, id):  # Cambiar pk por id
    humedad = get_object_or_404(Humedad, id=id)  # Cambiar pk por id
    if request.method == 'POST':
        humedad.delete()
        return redirect('listar_humedad')
    return render(request, 'laboratorio/ensayos/humedad/eliminar_humedad.html', {'humedad': humedad})

# Gráficos humedad
def graficos_humedad(request):
    # Obtener parámetros seleccionados (coinciden con HTML)
    id_proyectos = request.GET.getlist('id_proyectos')
    tipos_prospeccion = request.GET.getlist('tipos_prospeccion')
    areas = request.GET.getlist('areas')
    id_prospecciones = request.GET.getlist('id_prospecciones')

    # Depuración: verificar parámetros recibidos
    print("Parámetros recibidos:", request.GET)

    # Filtrar para opciones iniciales
    query = Humedad.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
        print("Tras id_proyectos:", query.count())
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
        print("Tras tipos_prospeccion:", query.count())
    if areas:
        query = query.filter(area__in=areas)
        print("Tras areas:", query.count())
    if id_prospecciones:
        query = query.filter(id_prospeccion__in=id_prospecciones)
        print("Tras id_prospecciones:", query.count())

    # Calcular opciones iniciales
    proyectos = query.values('id_proyecto').distinct()
    tipos_prospeccion_inicial = (query.values_list('tipo_prospeccion', flat=True)
                                 .distinct().exclude(tipo_prospeccion__isnull=True).exclude(tipo_prospeccion=''))
    areas_inicial = (query.values_list('area', flat=True)
                     .distinct().exclude(area__isnull=True).exclude(area=''))
    id_prospecciones_inicial = (query.values_list('id_prospeccion', flat=True)
                                .distinct().exclude(id_prospeccion__isnull=True).exclude(id_prospeccion=''))

    # Depuración: verificar opciones iniciales
    print("Proyectos iniciales:", list(proyectos))
    print("Tipos prospección iniciales:", list(tipos_prospeccion_inicial))
    print("Áreas iniciales:", list(areas_inicial))
    print("IDs prospección iniciales:", list(id_prospecciones_inicial))

    # Filtrar datos para gráficos
    humedades = Humedad.objects.all()
    if id_proyectos:
        humedades = humedades.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        humedades = humedades.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        humedades = humedades.filter(area__in=areas)
    if id_prospecciones:
        humedades = humedades.filter(id_prospeccion__in=id_prospecciones)

    # Crear DataFrame
    df = pd.DataFrame.from_records(humedades.values('id_proyecto', 'id_prospeccion', 'humedad', 'profundidad_promedio', 'area'))
    print("Datos en DataFrame:", df.shape)

    # Manejar caso de DataFrame vacío
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

    # Generar gráficos
    image_base64_area = generar_grafico_humedad_area(df)
    image_base64_prospeccion = generar_grafico_humedad_prospeccion(df)

    # Preparar contexto
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


from django.http import JsonResponse

def generar_grafico_humedad_area(df):
    areas_unicas = df['area'].unique()
    colores = {area: np.random.rand(3,) for area in areas_unicas}
    fig, ax = plt.subplots(figsize=(6, 6))
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
    fig.savefig(buffer, format='png', bbox_inches='tight', bbox_extra_artists=[legend])
    buffer.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

def generar_grafico_humedad_prospeccion(df):
    df['id_prospeccion'] = df['id_prospeccion'].astype(str)
    df['id_prospeccion_unico'] = df.groupby('id_prospeccion').cumcount() + 1
    df['etiqueta'] = df['id_prospeccion'] + '-' + df['id_prospeccion_unico'].astype(str)
    prospecciones_unicas = df['etiqueta'].unique()
    colores = {prospeccion: np.random.rand(3,) for prospeccion in prospecciones_unicas}
    fig, ax = plt.subplots(figsize=(6, 6))
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
    fig.savefig(buffer, format='png', bbox_inches='tight', bbox_extra_artists=[legend])
    buffer.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

def obtener_tipos_prospeccion_humedad(request):
    id_proyectos = request.GET.getlist('id_proyectos')
    query = Humedad.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    tipos_list = list(query.values_list('tipo_prospeccion', flat=True)
                     .distinct().exclude(tipo_prospeccion__isnull=True).exclude(tipo_prospeccion=''))
    print("Tipos devueltos:", tipos_list)
    return JsonResponse({'options': tipos_list}, safe=False)

def obtener_areas_humedad(request):
    id_proyectos = request.GET.getlist('id_proyectos')
    query = Humedad.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    areas_list = list(query.values_list('area', flat=True)
                     .distinct().exclude(area__isnull=True).exclude(area=''))
    print("Áreas devueltas:", areas_list)
    return JsonResponse({'options': areas_list}, safe=False)

def obtener_id_prospecciones_humedad(request):
    id_proyectos = request.GET.getlist('id_proyectos')
    tipos_prospeccion = request.GET.getlist('tipos_prospeccion')
    areas = request.GET.getlist('areas')
    query = Humedad.objects.all()
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    id_prospecciones_list = list(query.values_list('id_prospeccion', flat=True)
                                 .distinct().exclude(id_prospeccion__isnull=True).exclude(id_prospeccion=''))
    print("IDs prospección devueltos:", id_prospecciones_list)
    return JsonResponse({'options': id_prospecciones_list}, safe=False)

#### GRANULOMETRIA ##############################################

# Agregar granulometria
@login_required
def agregar_granulometria(request):
    proyectos = obtener_proyectos_prospecciones(request)
    if request.method == 'POST':
        post_data = request.POST.copy()
        proyecto_id = post_data.get('id_proyecto')
        if proyecto_id:
            try:
                proyecto = Proyectos.objects.get(id=proyecto_id)
                post_data['id_proyecto'] = proyecto
                print(f"Proyecto asignado: {proyecto}")
            except Proyectos.DoesNotExist:
                post_data['id_proyecto'] = None
                print("Proyecto no encontrado")
        prospeccion_id = post_data.get('id_prospeccion')
        if prospeccion_id:
            try:
                prospeccion = Prospecciones.objects.get(id_prospeccion=prospeccion_id)  # Cambiar n por id_prospeccion
                post_data['id_prospeccion'] = prospeccion
                print(f"Prospección asignada: {prospeccion}")
            except Prospecciones.DoesNotExist:
                post_data['id_prospeccion'] = None
                print("Prospección no encontrada")
        form = GranulometriaForm(post_data)
        if form.is_valid():
            granulometria = form.save(commit=False)
            granulometria.user = request.user
            granulometria.save()
            print("Formulario válido. Datos a guardar:", form.cleaned_data)
            return redirect('listar_granulometria')
        else:
            print("Formulario no válido. Errores:", form.errors)
    else:
        form = GranulometriaForm()
    return render(request, 'laboratorio/ensayos/granulometria/agregar_granulometria.html', {'form': form, 'proyectos': proyectos})


# Listar granulometria
def listar_granulometria(request):
    granulometrias = Granulometria.objects.all().order_by('id')  # Cambiar n por id
    query = request.GET.get('q', '')
    if query:
        granulometrias = granulometrias.filter(
            Q(id_proyecto__id__icontains=query) |
            Q(id_prospeccion__id_prospeccion__icontains=query) |  # Cambiar id_prospeccion por id_prospeccion
            Q(tipo_prospeccion__icontains=query)
        )

    paginator = Paginator(granulometrias, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'laboratorio/ensayos/granulometria/granulometria_table.html', {'page_obj': page_obj})
    return render(request, 'laboratorio/ensayos/granulometria/listar_granulometria.html', {'page_obj': page_obj, 'query': query})

# Exportar a excel
def export_to_excel_granulometria(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="granulometria.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Granulometria Data"
    headers = ['ID', 'Tipo prospeccion', 'ID Proyecto', 'ID Prospección', 'Área']  # Cambiar N por ID
    ws.append(headers)
    granulometrias = Granulometria.objects.all()
    for granulometria in granulometrias:
        id_proyecto = str(granulometria.id_proyecto)
        id_prospeccion = str(granulometria.id_prospeccion)
        ws.append([granulometria.id, granulometria.tipo_prospeccion, id_proyecto, id_prospeccion, granulometria.area])  # Cambiar n por id
    wb.save(response)
    return response

def export_to_pdf_granulometria(request):
    return HttpResponse("Exportar a PDF no está implementado")

# Ver granulometria
def ver_granulometria(request, id):  # Cambiar pk por id
    granulometria = get_object_or_404(Granulometria, id=id)  # Cambiar pk por id
    return render(request, 'laboratorio/ensayos/granulometria/ver_granulometria.html', {'granulometria': granulometria})

# Editar granulometria
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
            logger.error(f"Formulario no válido al editar granulometría {granulometria.id}: {form.errors}")
    else:
        form = GranulometriaForm(instance=granulometria)
    return render(request, 'laboratorio/ensayos/granulometria/editar_granulometria.html', {'form': form, 'granulometria': granulometria, 'proyectos': proyectos})

# Eliminar granulometria
def eliminar_granulometria(request, id):  # Cambiar pk por id
    granulometria = get_object_or_404(Granulometria, id=id)  # Cambiar pk por id
    if request.method == 'POST':
        granulometria.delete()
        return redirect('listar_granulometria')
    return render(request, 'laboratorio/ensayos/granulometria/eliminar_granulometria.html', {'granulometria': granulometria})




# Gráficos granulometria

# Vista principal para renderizar la página de gráficos de granulometría
def graficos_granulometria(request):
    # Obtener parámetros de la solicitud GET enviados por el usuario
    id_proyectos = request.GET.getlist('id_proyecto')  # Lista de IDs de proyectos seleccionados
    tipos_prospeccion = request.GET.getlist('tipo_prospeccion')  # Lista de tipos de prospección seleccionados
    areas = request.GET.getlist('area')  # Lista de áreas seleccionadas
    id_prospecciones = request.GET.getlist('id_prospeccion')  # Lista de IDs de prospección seleccionados

    # Consultar todos los registros de Granulometria como base para los filtros iniciales
    query = Granulometria.objects.all()

    # Aplicar filtros a la consulta inicial según los parámetros GET recibidos
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)  # Filtrar por proyectos seleccionados
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)  # Filtrar por tipos de prospección
    if areas:
        query = query.filter(area__in=areas)  # Filtrar por áreas
    if id_prospecciones:
        query = query.filter(id_prospeccion__in=id_prospecciones)  # Filtrar por IDs de prospección

    # Obtener valores distintos para los filtros iniciales basados en los datos filtrados
    proyectos = query.values('id_proyecto').distinct()  # Lista única de proyectos disponibles
    tipos_prospeccion_inicial = (query.values_list('tipo_prospeccion', flat=True)
                                .distinct()  # Tipos de prospección únicos
                                .exclude(tipo_prospeccion__isnull=True)  # Excluir nulos
                                .exclude(tipo_prospeccion=''))  # Excluir vacíos
    areas_inicial = (query.values_list('area', flat=True)
                     .distinct()  # Áreas únicas
                     .exclude(area__isnull=True)  # Excluir nulos
                     .exclude(area=''))  # Excluir vacíos
    id_prospecciones_inicial = (query.values_list('id_prospeccion', flat=True)
                                .distinct()  # IDs de prospección únicos
                                .exclude(id_prospeccion__isnull=True)  # Excluir nulos
                                .exclude(id_prospeccion=''))  # Excluir vacíos

    # Filtrar datos para los gráficos (usando la misma lógica que los filtros iniciales)
    granulometrias = Granulometria.objects.all()
    if id_proyectos:
        granulometrias = granulometrias.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        granulometrias = granulometrias.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        granulometrias = granulometrias.filter(area__in=areas)
    if id_prospecciones:
        granulometrias = granulometrias.filter(id_prospeccion__in=id_prospecciones)

    # Crear un DataFrame de Pandas con los datos filtrados para generar gráficos
    df = pd.DataFrame.from_records(granulometrias.values(
        'id_proyecto', 'id_prospeccion', 'n_0075', 'n_0110', 'n_0250', 'n_0420', 'n_0840',
        'n_2000', 'n_4760', 'n_9520', 'n_19000', 'n_25400', 'n_38100', 'n_50800', 'n_63500', 'n_75000', 'area'
    ))

    # Definir el contexto base para pasar a la plantilla HTML
    context = {
        'proyectos': proyectos,  # Lista de proyectos disponibles
        'tipos_prospeccion_inicial': tipos_prospeccion_inicial,  # Lista de tipos de prospección disponibles
        'areas_inicial': areas_inicial,  # Lista de áreas disponibles
        'id_prospecciones_inicial': id_prospecciones_inicial,  # Lista de IDs de prospección disponibles
        'selected_id_proyectos': json.dumps(id_proyectos),  # Proyectos seleccionados en formato JSON
        'selected_tipos_prospeccion': json.dumps(tipos_prospeccion),  # Tipos seleccionados en formato JSON
        'selected_areas': json.dumps(areas),  # Áreas seleccionadas en formato JSON
        'selected_id_prospecciones': json.dumps(id_prospecciones),  # IDs seleccionados en formato JSON
    }

    # Verificar si hay datos para graficar
    if df.empty:
        context['error'] = "No hay datos para graficar."  # Mensaje de error si no hay datos
        return render(request, 'laboratorio/ensayos/granulometria/graficos_granulometria.html', context)

    # Generar gráficos basados en el DataFrame filtrado
    image_base64_proyecto = generar_grafico_granulometria_area(df)  # Gráfico por proyecto
    image_base64_prospeccion = generar_grafico_granulometria_prospeccion(df)  # Gráfico por prospección

    # Actualizar el contexto con las imágenes generadas en base64
    context.update({
        'image_base64_proyecto': image_base64_proyecto,
        'image_base64_prospeccion': image_base64_prospeccion,
    })

    # Renderizar la plantilla HTML con el contexto completo
    return render(request, 'laboratorio/ensayos/granulometria/graficos_granulometria.html', context)


# Función para generar gráfico de granulometría por área/proyecto
def generar_grafico_granulometria_area(df):
    # Verificar que la columna 'id_prospeccion' esté presente en el DataFrame
    if 'id_prospeccion' not in df.columns:
        raise KeyError("La columna 'id_prospeccion' no está presente en los datos iniciales.")
    
    # Convertir id_proyecto a string y usarlo como etiqueta
    df['id_proyecto'] = df['id_proyecto'].astype(str)
    df['etiqueta'] = df['id_proyecto']
    proyectos_unicos = df['etiqueta'].unique()  # Obtener proyectos únicos
    
    # Asignar colores aleatorios a cada proyecto
    colores = {proyecto: np.random.rand(3,) for proyecto in proyectos_unicos}
    
    # Crear figura y eje para el gráfico
    fig, ax = plt.subplots()
    
    # Definir valores del eje X (tamaños de partícula en mm)
    x_values = np.array([0.075, 0.110, 0.250, 0.420, 0.840, 2.000, 4.760, 9.520, 19.000, 25.400, 38.100, 50.800, 63.500, 75.000])
    
    # Graficar una línea por cada registro de cada proyecto
    for proyecto in proyectos_unicos:
        datos_proyecto = df[df['etiqueta'] == proyecto]  # Filtrar datos por proyecto
        for i in range(len(datos_proyecto)):
            y_values = datos_proyecto.iloc[i, 2:16].values  # Obtener porcentajes de paso
            sorted_indices = np.argsort(x_values)[::-1]  # Ordenar en orden descendente
            x_values_sorted = x_values[sorted_indices]
            y_values_sorted = y_values[sorted_indices]
            # Dibujar la línea, asignar etiqueta solo a la primera línea por proyecto
            ax.plot(x_values_sorted, y_values_sorted, color=colores[proyecto], label=proyecto if i == 0 else "")

    # Configurar escala logarítmica en el eje X
    ax.set_xscale('log')
    ax.set_xlim(0.01, 100)  # Límites del eje X
    ax.xaxis.set_major_locator(LogLocator(base=10, numticks=10))  # Marcas principales
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs='auto', numticks=50))  # Marcas menores

    # Formatear etiquetas del eje X
    def log_format(x, _):
        if x < 1:
            return f"{x:.2f}"  # Mostrar decimales para valores < 1
        else:
            return f"{int(x)}"  # Enteros para valores >= 1
    ax.xaxis.set_major_formatter(FuncFormatter(log_format))
    ax.invert_xaxis()  # Invertir eje X (de mayor a menor)

    # Etiquetas y título
    ax.set_xlabel('Tamaño de partícula (mm)')
    ax.set_ylabel('Porcentaje que pasa (%)')
    ax.set_title('Distribución Granulométrica', pad=40)

    # Configurar leyenda
    handles, labels = ax.get_legend_handles_labels()
    max_legends = 27  # Limitar número de elementos en la leyenda
    if len(handles) > max_legends:
        handles = handles[:max_legends]
        labels = labels[:max_legends]
    ax.legend(handles, labels, loc='upper right', fontsize=8, ncol=1, columnspacing=0.5,
              handlelength=2, handletextpad=0.5, borderpad=0.5, framealpha=0.5, borderaxespad=0.5)

    # Líneas verticales para tamaños de tamiz
    ax.axvline(x=76.8, color='black', linestyle='--', linewidth=1, label='3')
    ax.axvline(x=19, color='black', linestyle='--', linewidth=1, label='3/4')
    ax.axvline(x=4.76, color='black', linestyle='--', linewidth=1, label='N°4')
    ax.axvline(x=0.42, color='black', linestyle='--', linewidth=1, label='N°40')
    ax.axvline(x=0.0749, color='black', linestyle='--', linewidth=1, label='N°200')
    ax.axhline(y=50, color='black', linestyle='--', linewidth=1, label='50')

    # Etiquetas sobre las líneas verticales
    ax.text(76.8, 106.5, '3', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(19, 106.5, '3/4', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(4.76, 106.5, '4', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))  # Corregido aquí
    ax.text(0.42, 106.5, '40', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(0.0749, 106.5, '200', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(140, 50, '50', color='black', va='bottom', ha='left', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))

    # Función auxiliar para agregar texto con caja
    def add_text_with_box(ax, x, y, text, color, pad=0.5, boxstyle='square'):
        ax.text(x, y, text, color=color, va='bottom', ha='center', fontsize=8,
                bbox=dict(facecolor='white', edgecolor="black", boxstyle=boxstyle, pad=pad))

    # Agregar etiquetas de clasificación de materiales
    add_text_with_box(ax, 19, 112, "    G    R    A    V    A     ", color='black', pad=0.3)
    add_text_with_box(ax, 0.60, 112, '      A         R         E         N         A      ', color='black', pad=0.3)
    add_text_with_box(ax, 0.025, 112, '   F   I   N   O   S   ', color='black', pad=0.3)

    # Agregar cuadrícula
    plt.grid(True)

    # Guardar gráfico en un buffer como imagen PNG
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches="tight", pad_inches=0.5)
    buffer.seek(0)
    plt.close()  # Cerrar la figura para liberar memoria

    # Convertir la imagen a base64 para incrustarla en HTML
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

# Función para generar gráfico de granulometría por prospección
def generar_grafico_granulometria_prospeccion(df):
    # Convertir id_prospeccion a string y crear etiquetas únicas
    df['id_prospeccion'] = df['id_prospeccion'].astype(str)
    df['id_prospeccion_unico'] = df.groupby('id_prospeccion').cumcount() + 1  # Numerar instancias duplicadas
    df['etiqueta'] = df['id_prospeccion'] + '-' + df['id_prospeccion_unico'].astype(str)
    prospecciones_unicas = df['etiqueta'].unique()  # Obtener prospecciones únicas

    # Asignar colores aleatorios a cada prospección
    colores = {prospeccion: np.random.rand(3,) for prospeccion in prospecciones_unicas}
    
    # Crear figura y eje para el gráfico
    fig, ax = plt.subplots()
    
    # Definir valores del eje X (tamaños de partícula en mm)
    x_values = np.array([0.075, 0.110, 0.250, 0.420, 0.840, 2.000, 4.760, 9.520, 19.000, 25.400, 38.100, 50.800, 63.500, 75.000])
    
    # Graficar una línea por cada prospección
    for prospeccion in prospecciones_unicas:
        datos_prospeccion = df[df['etiqueta'] == prospeccion]  # Filtrar datos por prospección
        y_values = datos_prospeccion.iloc[0, 2:16].values  # Obtener porcentajes de paso (primer registro)
        sorted_indices = np.argsort(x_values)[::-1]  # Ordenar en orden descendente
        x_values_sorted = x_values[sorted_indices]
        y_values_sorted = y_values[sorted_indices]
        ax.plot(x_values_sorted, y_values_sorted, color=colores[prospeccion], label=prospeccion)

    # Configurar escala logarítmica en el eje X
    ax.set_xscale('log')
    ax.set_xlim(0.01, 100)  # Límites del eje X
    ax.xaxis.set_major_locator(LogLocator(base=10, numticks=10))  # Marcas principales
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs='auto', numticks=50))  # Marcas menores

    # Formatear etiquetas del eje X
    def log_format(x, _):
        if x < 1:
            return f"{x:.2f}"  # Decimales para valores < 1
        else:
            return f"{int(x)}"  # Enteros para valores >= 1
    ax.xaxis.set_major_formatter(FuncFormatter(log_format))
    ax.invert_xaxis()  # Invertir eje X

    # Etiquetas y título
    ax.set_xlabel('Tamaño de partícula (mm)')
    ax.set_ylabel('Porcentaje que pasa (%)')
    ax.set_title('Distribución Granulométrica por Prospección', pad=40)

    # Configurar leyenda
    handles, labels = ax.get_legend_handles_labels()
    max_legends = 27  # Limitar número de elementos en la leyenda
    if len(handles) > max_legends:
        handles = handles[:max_legends]
        labels = labels[:max_legends]
    ax.legend(handles, labels, loc='upper right', fontsize=8, ncol=1, columnspacing=0.5,
              handlelength=2, handletextpad=0.5, borderpad=0.5, framealpha=0.5, borderaxespad=0.5)

    # Líneas verticales para tamaños de tamiz
    ax.axvline(x=76.8, color='black', linestyle='--', linewidth=1, label='3')
    ax.axvline(x=19, color='black', linestyle='--', linewidth=1, label='3/4')
    ax.axvline(x=4.76, color='black', linestyle='--', linewidth=1, label='N°4')
    ax.axvline(x=0.42, color='black', linestyle='--', linewidth=1, label='N°40')
    ax.axvline(x=0.0749, color='black', linestyle='--', linewidth=1, label='N°200')
    ax.axhline(y=50, color='black', linestyle='--', linewidth=1, label='50')

    # Etiquetas sobre las líneas verticales
    ax.text(76.8, 106.5, '3', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(19, 106.5, '3/4', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(4.76, 106.5, '4', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(0.42, 106.5, '40', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(0.0749, 106.5, '200', color='black', va='bottom', ha='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))
    ax.text(140, 50, '50', color='black', va='bottom', ha='left', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0))

    # Función auxiliar para agregar texto con caja
    def add_text_with_box(ax, x, y, text, color, pad=0.5, boxstyle='square'):
        ax.text(x, y, text, color=color, va='bottom', ha='center', fontsize=8,
                bbox=dict(facecolor='white', edgecolor="black", boxstyle=boxstyle, pad=pad))

    # Agregar etiquetas de clasificación de materiales
    add_text_with_box(ax, 19, 112, "    G    R    A    V    A     ", color='black', pad=0.3)
    add_text_with_box(ax, 0.60, 112, '      A         R         E         N         A      ', color='black', pad=0.3)
    add_text_with_box(ax, 0.025, 112, '   F   I   N   O   S   ', color='black', pad=0.3)

    # Agregar cuadrícula
    plt.grid(True)

    # Guardar gráfico en un buffer como imagen PNG
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches="tight", pad_inches=0.5)
    buffer.seek(0)
    plt.close()  # Cerrar la figura para liberar memoria

    # Convertir la imagen a base64 para incrustarla en HTML
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64


# Endpoint API para obtener tipos de prospección dinámicamente
def obtener_tipos_prospeccion_granulometria(request):
    # Obtener lista de IDs de proyectos desde la solicitud GET
    id_proyectos = request.GET.getlist('id_proyecto')
    # Consultar todos los registros de Granulometria
    tipos = Granulometria.objects.all()
    # Filtrar por proyectos si se proporcionan IDs
    if id_proyectos:
        tipos = tipos.filter(id_proyecto__in=id_proyectos)
    # Obtener lista única de tipos de prospección, excluyendo nulos y vacíos
    tipos_list = list(tipos.values_list('tipo_prospeccion', flat=True)
                     .distinct()
                     .exclude(tipo_prospeccion__isnull=True)
                     .exclude(tipo_prospeccion=''))
    # Imprimir para depuración
    print(f"Tipos para id_proyectos={id_proyectos}: {tipos_list}")
    # Devolver respuesta en formato JSON
    return JsonResponse({'options': tipos_list}, safe=False)

# Endpoint API para obtener áreas dinámicamente
def obtener_areas_granulometria(request):
    # Obtener lista de IDs de proyectos desde la solicitud GET
    id_proyectos = request.GET.getlist('id_proyecto')
    # Consultar todos los registros de Granulometria
    areas = Granulometria.objects.all()
    # Filtrar por proyectos si se proporcionan IDs
    if id_proyectos:
        areas = areas.filter(id_proyecto__in=id_proyectos)
    # Obtener lista única de áreas, excluyendo nulos y vacíos
    areas_list = list(areas.values_list('area', flat=True)
                     .distinct()
                     .exclude(area__isnull=True)
                     .exclude(area=''))
    # Imprimir para depuración
    print(f"Áreas para id_proyectos={id_proyectos}: {areas_list}")
    # Devolver respuesta en formato JSON
    return JsonResponse({'options': areas_list}, safe=False)

# Endpoint API para obtener IDs de prospección dinámicamente
def obtener_id_prospecciones_granulometria(request):
    # Obtener parámetros de la solicitud GET
    id_proyectos = request.GET.getlist('id_proyecto')
    tipos_prospeccion = request.GET.getlist('tipo_prospeccion')
    areas = request.GET.getlist('area')
    # Consultar todos los registros de Granulometria
    query = Granulometria.objects.all()
    # Aplicar filtros según parámetros recibidos
    if id_proyectos:
        query = query.filter(id_proyecto__in=id_proyectos)
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    # Obtener lista única de IDs de prospección, excluyendo nulos y vacíos
    id_prospecciones_list = list(query.values_list('id_prospeccion', flat=True)
                                .distinct()
                                .exclude(id_prospeccion__isnull=True)
                                .exclude(id_prospeccion=''))
    # Imprimir para depuración
    print(f"ID Prospecciones para id_proyectos={id_proyectos}, tipos={tipos_prospeccion}, areas={areas}: {id_prospecciones_list}")
    # Devolver respuesta en formato JSON
    return JsonResponse({'options': id_prospecciones_list}, safe=False)

# Endpoint API para obtener proyectos dinámicamente
def obtener_id_proyecto_granulometria(request):
    # Obtener parámetros de la solicitud GET
    tipos_prospeccion = request.GET.getlist('tipo_prospeccion')
    areas = request.GET.getlist('area')
    id_prospecciones = request.GET.getlist('id_prospeccion')
    # Consultar todos los registros de Granulometria
    query = Granulometria.objects.all()
    # Aplicar filtros según parámetros recibidos
    if tipos_prospeccion:
        query = query.filter(tipo_prospeccion__in=tipos_prospeccion)
    if areas:
        query = query.filter(area__in=areas)
    if id_prospecciones:
        query = query.filter(id_prospeccion__in=id_prospecciones)
    # Obtener lista única de proyectos, excluyendo nulos y vacíos
    proyectos_list = list(query.values_list('id_proyecto', flat=True)
                         .distinct()
                         .exclude(id_proyecto__isnull=True)
                         .exclude(id_proyecto=''))
    # Imprimir para depuración
    print(f"Proyectos para tipos={tipos_prospeccion}, areas={areas}, id_prospecciones={id_prospecciones}: {proyectos_list}")
    # Devolver respuesta en formato JSON
    return JsonResponse({'options': proyectos_list}, safe=False)






#### MUESTREO ##############################################

# Agregar muestreo
@login_required
def agregar_muestreo(request):
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
        prospeccion_id = post_data.get('id_prospeccion')
        if prospeccion_id:
            try:
                prospeccion = Prospecciones.objects.get(id_prospeccion=prospeccion_id)  # Cambiar n por id_prospeccion
                post_data['id_prospeccion'] = prospeccion
            except Prospecciones.DoesNotExist:
                post_data['id_prospeccion'] = None
        form = MuestreoForm(post_data)
        if form.is_valid():
            muestreo = form.save(commit=False)
            muestreo.user = request.user
            muestreo.save()
            return redirect('listar_muestreo')
    else:
        form = MuestreoForm()
    return render(request, 'terreno/muestreo/agregar_muestreo.html', {'form': form, 'proyectos': proyectos})

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

    paginator = Paginator(muestreos, 10)
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

# Agregar programa
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
                print(f"Proyecto asignado: {proyecto}")
            except Proyectos.DoesNotExist:
                post_data['id_proyecto'] = None
                print("Proyecto no encontrado")
        prospeccion_id = post_data.get('id_prospeccion')
        if prospeccion_id:
            try:
                prospeccion = Prospecciones.objects.get(id_prospeccion=prospeccion_id)  # Cambiar n por id_prospeccion
                post_data['id_prospeccion'] = prospeccion
                print(f"Prospección asignada: {prospeccion}")
            except Prospecciones.DoesNotExist:
                post_data['id_prospeccion'] = None
                print("Prospección no encontrada")
        form = ProgramaForm(post_data)
        if form.is_valid():
            programa = form.save(commit=False)
            programa.user = request.user
            programa.save()
            print("Formulario válido. Datos a guardar:", form.cleaned_data)
            return redirect('listar_programa')
        else:
            print("Formulario no válido. Errores:", form.errors)
    else:
        form = ProgramaForm()
    return render(request, 'laboratorio/programa/agregar_programa.html', {'form': form, 'proyectos': proyectos})

# Traer el campo de área automáticamente
def get_area(request):
    prospeccion_id = request.GET.get('prospeccion_id')
    try:
        prospeccion = Prospecciones.objects.get(id_prospeccion=prospeccion_id)  # Cambiar n por id_prospeccion
        area = prospeccion.area
    except Prospecciones.DoesNotExist:
        area = ''
    return JsonResponse({'area': area})

# Listar programas
def listar_programa(request):
    programas = Programa.objects.all().order_by('id')  # Cambiar n por id
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

# Exportar a excel
def export_to_excel_programa(request):
    programas = Programa.objects.all().values()
    df = pd.DataFrame(programas)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=programas.xlsx'
    df.to_excel(response, index=False)
    return response

def export_to_pdf_programa(request):
    pass

# Ver programa
def ver_programa(request, id):  # Cambiar n por id
    programa = get_object_or_404(Programa, id=id)  # Cambiar pk por id y corregir "programa" a "Programa"
    return render(request, 'laboratorio/programa/listar_programa.html', {'programa': programa})

# Editar programa
@login_required
def editar_programa(request, id):  # Cambiar n por id
    programa = get_object_or_404(Programa, id=id)  # Cambiar pk por id
    proyectos = Proyectos.objects.all()
    prospecciones = Prospecciones.objects.all()
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
        'proyectos': proyectos,
        'prospecciones': prospecciones
    })

# Eliminar programa
def eliminar_programa(request, id):  # Cambiar n por id
    programa = get_object_or_404(Programa, id=id)  # Cambiar pk por id y corregir "programa" a "Programa"
    programa.delete()
    return redirect('listar_programa')

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
    plt.legend(loc='upper right')
    for i, (total, avance) in enumerate(zip(objetivo_counts, avance_counts)):
        plt.text(total + 0.5, i, f'{avance}', va='center', color='blue')
    plt.tight_layout()

    buffer_barras = BytesIO()
    plt.savefig(buffer_barras, format='png')
    buffer_barras.seek(0)
    image_base64_barras = base64.b64encode(buffer_barras.getvalue()).decode('utf-8')
    plt.close()

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

    paginator = Paginator(nomina_list, 10)  # 10 registros por página
    page_number = request.GET.get('page')
    nomina_list = paginator.get_page(page_number)
    return render(request, 'nomina/listar_nomina.html', {'nomina_list': nomina_list, 'consulta': consulta})

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

# Exportar a Excel
logger = logging.getLogger(__name__)

@login_required
def export_to_excel_nomina(request):
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Roster"

        # Definir el rango de fechas (1 de enero al 28 de febrero de 2025)
        fecha_inicio = date(2025, 1, 1)  # Usar date en lugar de datetime
        fecha_fin = date(2025, 2, 28)
        dias = (fecha_fin - fecha_inicio).days + 1
        dias_semana = ['L', 'M', 'X', 'J', 'V', 'S', 'D']

        # Encabezados
        base_headers = ["ID Proyecto", "Nombre", "RUT", "Cargo", "Turno"]
        date_headers = [
            f"{dias_semana[i % 7]}-{fecha_inicio + timedelta(days=i):%d-%m-%y}"
            for i in range(dias)
        ]
        headers = base_headers + date_headers + ["Total Trabajador"]
        ws.append(headers)

        # Obtener todas las nóminas y sus rosters
        nominas = Nomina.objects.prefetch_related('rosters', 'id_proyecto').all()
        totales_por_dia = [0.0] * dias

        for nomina in nominas:
            row = [
                nomina.id_proyecto.nombre if nomina.id_proyecto else "N/A",
                f"{nomina.nombre} {nomina.apellido}",
                nomina.rut,
                nomina.cargo,
                nomina.turno if nomina.turno else "N/A"
            ]
            
            # Obtener los rosters o calcular horas si no existen
            rosters = nomina.rosters.filter(fecha__range=[fecha_inicio, fecha_fin]).order_by('fecha')
            roster_dict = {roster.fecha: float(roster.horas_asignadas) for roster in rosters}
            
            # Rellenar las horas por día
            total_trabajador = 0.0
            for i in range(dias):
                fecha = fecha_inicio + timedelta(days=i)
                horas = roster_dict.get(fecha, nomina.get_hours_for_date(fecha))
                row.append(horas)
                total_trabajador += horas
                totales_por_dia[i] += horas
            
            row.append(total_trabajador)
            ws.append(row)

        # Agregar fila de totales por día
        total_row = ["Total por Día", "", "", "", ""]
        total_row.extend(totales_por_dia)
        total_row.append("")
        ws.append(total_row)

        # Ajustar ancho de columnas
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min((max_length + 2), 15)
            ws.column_dimensions[column].width = adjusted_width

        # Crear y retornar la respuesta
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="roster.xlsx"'
        wb.save(response)
        return response

    except Exception as e:
        logger.error(f"Error al generar archivo Excel: {str(e)}")
        return HttpResponse(f"Error al generar el archivo Excel: {str(e)}", status=500)
            
# Exportar a PDF
logger = logging.getLogger(__name__)

@login_required
def export_to_pdf_nomina(request):
    try:
        # Crear el objeto HttpResponse para PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="roster.pdf"'
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Definir el rango de fechas (1 de enero al 28 de febrero de 2025)
        fecha_inicio = datetime(2025, 1, 1)
        fecha_fin = datetime(2025, 2, 28)
        dias = (fecha_fin - fecha_inicio).days + 1
        dias_semana = ['L', 'M', 'X', 'J', 'V', 'S', 'D']

        # Encabezados
        base_headers = ["ID Proyecto", "Nombre", "RUT", "Cargo", "Turno"]
        date_headers = [
            f"{dias_semana[i % 7]}-{fecha_inicio + timedelta(days=i):%d-%m-%y}"
            for i in range(dias)
        ]
        headers = base_headers + date_headers + ["Total Trabajador"]
        data = [headers]

        # Obtener todas las nóminas y sus rosters
        nominas = Nomina.objects.prefetch_related('rosters', 'id_proyecto').all()
        totales_por_dia = [0.0] * dias

        for nomina in nominas:
            row = [
                nomina.id_proyecto.nombre if nomina.id_proyecto else "N/A",
                f"{nomina.nombre} {nomina.apellido}",
                nomina.rut,
                nomina.cargo,
                nomina.turno if nomina.turno else "N/A"
            ]
            
            # Obtener los rosters o calcular horas si no existen
            rosters = nomina.rosters.filter(fecha__range=[fecha_inicio, fecha_fin]).order_by('fecha')
            roster_dict = {roster.fecha: float(roster.horas_asignadas) for roster in rosters}
            
            # Rellenar las horas por día
            total_trabajador = 0.0
            for i in range(dias):
                fecha = fecha_inicio + timedelta(days=i)
                horas = roster_dict.get(fecha, nomina.get_hours_for_date(fecha))
                row.append(str(horas))  # Convertir a string para reportlab
                total_trabajador += horas
                totales_por_dia[i] += horas
            
            row.append(str(total_trabajador))
            data.append(row)

        # Agregar fila de totales por día
        total_row = ["Total por Día", "", "", "", ""]
        total_row.extend([str(total) for total in totales_por_dia])
        total_row.append("")
        data.append(total_row)

        # Crear la tabla
        table = Table(data, colWidths=[80, 120, 80, 60, 80] + [40] * (dias + 1))
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

        # Generar el PDF
        doc.build(elements)
        return response

    except Exception as e:
        logger.error(f"Error al generar archivo PDF: {str(e)}")
        return HttpResponse(f"Error al generar el archivo PDF: {str(e)}", status=500)


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



from .models import Granulometria
print(Granulometria.objects.values('tipo_prospeccion', 'area', 'id_prospeccion').distinct())
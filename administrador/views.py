from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, F
import pandas as pd
from .models import Usuarios, Proyectos, Prospecciones, Humedad, Area, Muestreo
from .forms import forms  # Asegúrate de importar tu formulario
from datetime import datetime
from .forms import LoginForm, ProyectoEditForm, ProspeccionesForm, HumedadForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
import csv
from django.http import HttpResponse
from openpyxl import Workbook
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from django.http import JsonResponse
from .forms import ProyectoEditForm, MuestreoForm
from django.db.models import Q, CharField, TextField, DateField, DateTimeField
from django.apps import apps



# Create your views here.

TEMPLATE_DIR = (
    'os.path.join(BASE_DIR, "templates),'
)


#### INICIO DE SESION  #############################################################################

# Inicio de sesion
def home_view(request):
    return render(request, 'home.html')

# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Autenticación usando el email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')  # Redirige a index_master.html
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


#### USUARIOS #############################################################################

## crear nuevo registros de usuarios
def index(request):                
    return render(request,"index.html")

@login_required  # Asegura que solo usuarios autenticados accedan a la vista
def agregar_usuarios(request):
    if request.method == 'POST':
        if request.POST.get('empresa') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('email') and request.POST.get('telefono'):
            u = Usuarios()
            u.empresa = request.POST.get('empresa')
            u.nombre = request.POST.get('nombre')
            u.apellido = request.POST.get('apellido')
            u.email = request.POST.get('email')
            u.telefono = request.POST.get('telefono')
            u.usuario_creador = request.user  # Asigna el usuario que realiza la operación
            u.save()
            return redirect('listar_usuarios')
        else:
            return render(request, 'usuarios/agregar_usuarios.html', {'error': 'Todos los campos son obligatorios.'})
    return render(request, 'usuarios/agregar_usuarios.html')


#listar usuario############################################## 
def listar_usuarios(request):
    users = Usuarios.objects.all()
    datos = {'usuarios' : users}
    return render(request, "usuarios/listar_usuarios.html", datos)

###Para descargar adjuntos XLS y .PDF
def export_to_excel(request):
    proyectos = Proyectos.objects.all()
    df = pd.DataFrame(list(proyectos.values()))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=proyectos.xlsx'
    df.to_excel(response, index=False)
    return response

def export_to_pdf(request):
    # Implementación de exportación a PDF (puedes usar ReportLab o WeasyPrint)
    pass


#Editar usuario############################################## 
def editar_usuarios(request):
    if request.method == 'POST':
        user_id = request.POST.get('n')
        if user_id and all(key in request.POST for key in ['empresa', 'nombre', 'apellido', 'email', 'telefono']):
            u = get_object_or_404(Usuarios, n=n)
            u.empresa = request.POST.get('empresa')
            u.nombre = request.POST.get('nombre')
            u.apellido = request.POST.get('apellido')
            u.email = request.POST.get('email')
            u.telefono = request.POST.get('telefono')
            u.save()
            return redirect('listar_usuarios')
    usuarios = Usuarios.objects.all()
    return render(request, 'usuarios/editar_usuarios.html', {'usuarios': usuarios})

#Eliminar usuario############################################## 
def eliminar_usuarios(request):
    if request.method == 'POST':
        if request.POST.get('n'):
            id_a_borrar = request.POST.get('n')
            registro = get_object_or_404(Usuarios, n=id_a_borrar)
            registro.delete()
            return redirect('listar_usuarios')
    usuarios = Usuarios.objects.all()
    return render(request, 'usuarios/eliminar_usuarios.html', {'usuarios': usuarios})

 
    

#### PROYECTO ##############################################

#Agregar proyecto############################################## 
@login_required #Trael el numero de usuario
def agregar_proyectos(request):
    if request.method == 'POST':
        form = ProyectoEditForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.user = request.user  # Captura el usuario que realiza la operación
            proyecto.save()
            return redirect('listar_proyectos')  # Cambia a la vista deseada
    else:
        form = ProyectoEditForm()

    return render(request, 'proyectos/agregar_proyectos.html', {'form': form})


# Listar proyecto##############################################
def listar_proyectos(request):
    # Obtener todos los proyectos y ordenarlos por un campo específico, por ejemplo, 'id'
    proyectos = Proyectos.objects.all().order_by('id')  # Asegúrate de usar el campo que desees para ordenar
    
    # Obtener el término de búsqueda
    query = request.GET.get('q', '')  # Obtener el término de búsqueda, o una cadena vacía si no existe
    if query:
        # Obtener el modelo Proyectos
        Proyectos_model = apps.get_model('administrador', 'Proyectos')
        
        # Obtener todos los nombres de los campos del modelo Proyectos
        fields = [field.name for field in Proyectos_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField))]
        
        # Crear un objeto Q vacío
        query_filter = Q()
        
        # Iterar sobre todos los campos y agregar un filtro Q para cada campo
        for field in fields:
            if isinstance(Proyectos_model._meta.get_field(field), (DateField, DateTimeField)):
                # Convertir fechas a cadenas y aplicar icontains
                query_filter |= Q(**{f"{field}__year__icontains": query})  # Filtrar por año
                query_filter |= Q(**{f"{field}__month__icontains": query})  # Filtrar por mes
                query_filter |= Q(**{f"{field}__day__icontains": query})  # Filtrar por día
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        
        # Aplicar el filtro al queryset
        proyectos = proyectos.filter(query_filter)

    # Configurar la paginación
    paginator = Paginator(proyectos, 10)  # 10 proyectos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Verificar si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'proyectos/proyectos_table.html', {'page_obj': page_obj})

    return render(request, 'proyectos/listar_proyectos.html', {'page_obj': page_obj, 'query': query})

#Ver proyecto############################################## 
def ver_proyectos(request, n):
    proyecto = get_object_or_404(Proyectos, pk=n)
    return render(request, 'ver_proyectos.html', {'proyecto': proyecto})

#Eliminar proyecto############################################## 
def eliminar_proyectos(request, n):
    proyecto = get_object_or_404(Proyectos, pk=n)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('listar_proyectos')
    return render(request, 'eliminar_proyectos.html', {'proyecto': proyecto})


def grafico(request):
    texto = "¡Hola! Esta es una vista de texto simple."
    return render(request, 'grafico.html', {'grafico': grafico})

#Editar proyecto############################################## 
def editar_proyectos(request, n):
    # Obtén el proyecto correspondiente al campo n
    proyecto = get_object_or_404(Proyectos, n=n)

    if request.method == 'POST':
        # Actualiza los campos del proyecto con los datos del formulario
        proyecto.pm = request.POST.get('pm')
        proyecto.empresa = request.POST.get('empresa')
        proyecto.nombre = request.POST.get('nombre')
        proyecto.alcance = request.POST.get('alcance')
        proyecto.fecha_inicio = request.POST.get('fecha_inicio')
        proyecto.fecha_termino = request.POST.get('fecha_termino')
        proyecto.save()  # Guarda los cambios en la base de datos
        return redirect('listar_proyectos')  # Redirige a la lista de proyectos

    # Si la solicitud es GET, muestra el formulario con los datos actuales del proyecto
    return render(request, 'proyectos/editar_proyectos.html', {'proyecto': proyecto})




#### PROSPECCIONES ##############################################

#Agregar prospeccione##############################################
@login_required  # Asegura que solo usuarios autenticados accedan a la vista
def agregar_prospecciones(request):
    # Initialize the form
    form = ProspeccionesForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            prospeccion = form.save(commit=False)  # No guardar todavía el objeto
            prospeccion.user = request.user  # Asigna el usuario que realiza la operación
            prospeccion.save()  # Ahora guarda el objeto

            image = request.FILES.get('image')
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                uploaded_file_url = fs.url(filename)
                print(f'Archivo guardado en: {uploaded_file_url}')  # Mensaje de depuración
            else:
                print('No se recibió imagen.')  # Mensaje de depuración adicional
            return redirect('listar_prospecciones')  # Redirigir después de guardar
        else:
            print('Formulario no es válido')  # Mensaje de depuración
            print(form.errors)  # Mostrar errores del formulario

    # Para el caso de GET o si el formulario no es válido, renderizar el formulario
    return render(request, 'prospecciones/agregar_prospecciones.html', {'form': form})


# Listar prospecciones##############################################
def listar_prospecciones(request):
    # Obtener todas las prospecciones y ordenarlas por un campo específico, por ejemplo, 'n'
    prospecciones = Prospecciones.objects.all().order_by('n')  # Asegúrate de usar el campo que desees para ordenar
    
    # Obtener el término de búsqueda
    query = request.GET.get('q', '')  # Obtener el término de búsqueda, o una cadena vacía si no existe
    if query:
        # Obtener el modelo Prospecciones
        Prospecciones_model = apps.get_model('administrador', 'Prospecciones')
        
        # Obtener todos los nombres de los campos del modelo Prospecciones
        fields = [field.name for field in Prospecciones_model._meta.get_fields() if isinstance(field, (CharField, TextField, DateField, DateTimeField))]
        
        # Crear un objeto Q vacío
        query_filter = Q()
        
        # Iterar sobre todos los campos y agregar un filtro Q para cada campo
        for field in fields:
            if isinstance(Prospecciones_model._meta.get_field(field), (DateField, DateTimeField)):
                # Convertir fechas a cadenas y aplicar icontains
                query_filter |= Q(**{f"{field}__year__icontains": query})  # Filtrar por año
                query_filter |= Q(**{f"{field}__month__icontains": query})  # Filtrar por mes
                query_filter |= Q(**{f"{field}__day__icontains": query})  # Filtrar por día
            else:
                query_filter |= Q(**{f"{field}__icontains": query})
        
        # Aplicar el filtro al queryset
        prospecciones = prospecciones.filter(query_filter)

    # Configurar la paginación
    paginator = Paginator(prospecciones, 10)  # 10 prospecciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Verificar si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'prospecciones/prospecciones_table.html', {'page_obj': page_obj})

    return render(request, 'prospecciones/listar_prospecciones.html', {'page_obj': page_obj, 'query': query})

# Exportar el arhivo excel ######
def export_to_excel_prospecciones(request):
    # Obtener todas las prospecciones
    prospecciones = Prospecciones.objects.all().values()  # Obtener todos los campos

    # Crear un DataFrame de pandas
    df = pd.DataFrame(prospecciones)

    # Crear una respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=prospecciones.xlsx'

    # Guardar el DataFrame en el archivo Excel
    df.to_excel(response, index=False)

    return response




def export_to_pdf_prospecciones(request):
    # Lógica para exportar prospecciones a PDF
    pass

#ver prospeccione##############################################
def ver_prospeccion(request, n):
    prospeccion = get_object_or_404(Prospecciones, pk=n)
    return render(request, 'prospecciones/ver_prospeccion.html', {'prospeccion': prospeccion})

#editar prospeccione##############################################
def editar_prospeccion(request, n):
    # Lógica para editar prospecciones
    pass

#eliminar prospeccione##############################################
def eliminar_prospeccion(request, n):
    prospeccion = get_object_or_404(Prospecciones, pk=n)
    prospeccion.delete()
    return redirect('listar_prospecciones')  # Redirigir después de la eliminación



####MUESTREO"################################################
#agregar muestreo (filtros)##############################################
def obtener_tipos_prospeccion(request):
    id_proyecto = request.GET.get('id_proyecto')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto).values('tipo_prospeccion').distinct()
    tipos_prospeccion = {pros['tipo_prospeccion']: pros['tipo_prospeccion'] for pros in prospecciones}
    return JsonResponse(tipos_prospeccion)

def obtener_id_prospecciones(request):
    id_proyecto = request.GET.get('id_proyecto')
    tipo_prospeccion = request.GET.get('tipo_prospeccion')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto, tipo_prospeccion=tipo_prospeccion).values('n', 'id_prospeccion').distinct()
    id_prospecciones = {pros['n']: pros['id_prospeccion'] for pros in prospecciones}
    return JsonResponse(id_prospecciones)

def get_area(request):
    prospeccion_id = request.GET.get('prospeccion_id')
    try:
        prospeccion = Prospecciones.objects.get(n=prospeccion_id)
        area = prospeccion.area
    except Prospecciones.DoesNotExist:
        area = ''
    return JsonResponse({'area': area})

#agregar muestreo##############################################
@login_required
def agregar_muestreo(request):
    proyectos = Proyectos.objects.all()

    if request.method == 'POST':
        post_data = request.POST.copy()

        # Convertir el id_proyecto a una instancia de Proyectos utilizando el campo correcto
        proyecto_id = post_data.get('id_proyecto')
        if proyecto_id:
            try:
                proyecto = Proyectos.objects.get(id=proyecto_id)
                post_data['id_proyecto'] = proyecto  # Asignar la instancia del proyecto
                print(f"Proyecto asignado: {proyecto}")
            except Proyectos.DoesNotExist:
                post_data['id_proyecto'] = None
                print("Proyecto no encontrado")

        # Convertir el id_prospeccion a una instancia de Prospecciones utilizando el campo correcto
        prospeccion_id = post_data.get('id_prospeccion')
        if prospeccion_id:
            try:
                prospeccion = Prospecciones.objects.get(n=prospeccion_id)
                post_data['id_prospeccion'] = prospeccion  # Asignar la instancia de prospección
                print(f"Prospección asignada: {prospeccion}")
            except Prospecciones.DoesNotExist:
                post_data['id_prospeccion'] = None
                print("Prospección no encontrada")

        form = MuestreoForm(post_data)
        if form.is_valid():
            muestreo = form.save(commit=False)  # No guardar todavía el objeto
            muestreo.user = request.user  # Asignar el usuario que realiza la operación
            muestreo.save()  # Ahora guardar el objeto

            print("Formulario válido. Datos a guardar:", form.cleaned_data)
            return redirect('listar_muestreo')
        else:
            print("Formulario no válido. Errores:", form.errors)
    else:
        form = MuestreoForm()
    
    return render(request, 'prospecciones/muestreo/agregar_muestreo.html', {'form': form, 'proyectos': proyectos})


#listar ##############################################

def listar_muestreo(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda, o una cadena vacía si no existe
    if query:
        # Filtrar por múltiples columnas usando icontains para búsqueda parcial
        muestreo_list = Muestreo.objects.filter(
            Q(id_proyecto__id__icontains=query) |  # Busca en el campo 'id' del modelo 'Proyectos'
            Q(id_prospeccion__id_prospeccion__icontains=query) |  # Busca en el campo 'id_prospeccion' del modelo 'Prospecciones'
            Q(tipo_prospeccion__icontains=query) |
            Q(fecha_muestreo__icontains=query) |
            Q(n_muestra__icontains=query) |
            Q(embalaje__icontains=query) |
            Q(peso__icontains=query) |
            Q(cota_desde__icontains=query) |
            Q(cota_hasta__icontains=query) |
            Q(estrato__icontains=query) |
            Q(tipo__icontains=query) |
            Q(area__icontains=query)
        )
    else:
        muestreo_list = Muestreo.objects.all()

    paginator = Paginator(muestreo_list, 10)  # Número de elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'prospecciones/muestreo/listar_muestreo.html', {'page_obj': page_obj, 'query': query})



def export_to_excel_muestreo(request):
    # Lógica para exportar muestreo a Excel
    pass

def export_to_pdf_muestreo(request):
    # Lógica para exportar muestreo a PDF
    pass


def ver_muestreo(request, n):
    muestreo = get_object_or_404(Muestreo, pk=n)
    return render(request, 'prospecciones/muestreo/ver_muestreo.html', {'muestreo': muestreo})


@login_required  # Asegura que solo usuarios autenticados accedan a la vista
def editar_muestreo(request, n):
    muestreo = get_object_or_404(Muestreo, pk=n)
    form = MuestreoForm(request.POST or None, request.FILES or None, instance=muestreo)

    if request.method == 'POST':
        if form.is_valid():
            muestreo = form.save(commit=False)
            muestreo.user = request.user  # Asigna el usuario que realiza la operación
            muestreo.save()  # Guarda los cambios
            return redirect('listar_muestreo')  # Redirigir después de guardar
        else:
            print('Formulario no es válido')  # Mensaje de depuración
            print(form.errors)  # Mostrar errores del formulario

    return render(request, 'prospecciones/muestreo/editar_muestreo.html', {'form': form})



@login_required  # Asegura que solo usuarios autenticados accedan a la vista
def eliminar_muestreo(request, pk):
    muestreo = get_object_or_404(Muestreo, pk=pk)
    if request.method == 'POST':
        muestreo.delete()
        return redirect('listar_muestreo')
    return render(request, 'prospecciones/muestreo/listar_muestreo.html', {'muestreo': muestreo})




############ENSAYOS LABORATORIO########################################

####HUMEDAD"################################################

#Agregar humedad##############################################
##Para los filtros
def obtener_tipos_prospeccion(request):
    id_proyecto = request.GET.get('id_proyecto')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto).values('tipo_prospeccion').distinct()
    tipos_prospeccion = {pros['tipo_prospeccion']: pros['tipo_prospeccion'] for pros in prospecciones}
    return JsonResponse(tipos_prospeccion)

def obtener_id_prospecciones(request):
    id_proyecto = request.GET.get('id_proyecto')
    tipo_prospeccion = request.GET.get('tipo_prospeccion')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto, tipo_prospeccion=tipo_prospeccion).values('n', 'id_prospeccion').distinct()
    id_prospecciones = {pros['n']: pros['id_prospeccion'] for pros in prospecciones}
    return JsonResponse(id_prospecciones)

##Agregar humedad
@login_required  # Asegura que solo usuarios autenticados accedan a la vista
def agregar_humedad(request):
    proyectos = Proyectos.objects.all()

    if request.method == 'POST':
        post_data = request.POST.copy()

        # Convertir el id_proyecto a una instancia de Proyectos utilizando el campo correcto
        proyecto_id = post_data.get('id_proyecto')
        if proyecto_id:
            try:
                proyecto = Proyectos.objects.get(id=proyecto_id)
                post_data['id_proyecto'] = proyecto  # Asignar la instancia del proyecto
                print(f"Proyecto asignado: {proyecto}")
            except Proyectos.DoesNotExist:
                post_data['id_proyecto'] = None
                print("Proyecto no encontrado")

        # Convertir el id_prospeccion a una instancia de Prospecciones utilizando el campo correcto
        prospeccion_id = post_data.get('id_prospeccion')
        if prospeccion_id:
            try:
                prospeccion = Prospecciones.objects.get(n=prospeccion_id)
                post_data['id_prospeccion'] = prospeccion  # Asignar la instancia de prospección
                print(f"Prospección asignada: {prospeccion}")
            except Prospecciones.DoesNotExist:
                post_data['id_prospeccion'] = None
                print("Prospección no encontrada")

        form = HumedadForm(post_data)
        if form.is_valid():
            humedad = form.save(commit=False)  # No guardar todavía el objeto
            humedad.user = request.user  # Asignar el usuario que realiza la operación
            humedad.save()  # Ahora guardar el objeto

            print("Formulario válido. Datos a guardar:", form.cleaned_data)
            return redirect('listar_humedad')
        else:
            print("Formulario no válido. Errores:", form.errors)
    else:
        form = HumedadForm()
    
    return render(request, 'laboratorio/ensayos/humedad/agregar_humedad.html', {'form': form, 'proyectos': proyectos})


##Traer el campo de area automaticamente
def get_area(request):
    prospeccion_id = request.GET.get('prospeccion_id')
    try:
        prospeccion = Prospecciones.objects.get(n=prospeccion_id)
        area = prospeccion.area
    except Prospecciones.DoesNotExist:
        area = ''
    return JsonResponse({'area': area})



#Listar humedad############################
def listar_humedad(request):
    humedades = Humedad.objects.all().order_by('n')
    
    # Obtener el término de búsqueda
    query = request.GET.get('q', '')  # Obtener el término de búsqueda, o una cadena vacía si no existe
    if query:
        # Filtrar por múltiples columnas usando icontains para búsqueda parcial
        humedades = humedades.filter(
            Q(id_proyecto__id__icontains=query) |  # Busca en el campo 'id' del modelo 'Proyectos'
            Q(id_prospeccion__id_prospeccion__icontains=query) |  # Busca en el campo 'id_prospeccion' del modelo 'Prospecciones'
            Q(tipo_prospeccion__icontains=query) |
            Q(humedad__icontains=query) |
            Q(profundidad_promedio__icontains=query) |
            Q(area__icontains=query)
        )

    # Configurar la paginación
    paginator = Paginator(humedades, 10)  # 10 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Verificar si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'laboratorio/ensayos/humedad/humedad_table.html', {'page_obj': page_obj})

    return render(request, 'laboratorio/ensayos/humedad/listar_humedad.html', {'page_obj': page_obj, 'query': query})


#Exportar lista humedad excel (dentro de listar humedad)
def export_to_excel_humedad(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="humedad.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Humedad Data"

    # Escribir encabezados
    headers = ['N', 'Tipo prospeccion', 'ID Proyecto', 'ID Prospección', 'Humedad', 'Profundidad Promedio', 'area']
    ws.append(headers)

    # Escribir datos
    humedades = Humedad.objects.all()
    for humedad in humedades:
        # Convertir los ForeignKey a cadenas
        id_proyecto = str(humedad.id_proyecto)
        id_prospeccion = str(humedad.id_prospeccion)
        ws.append([humedad.n, humedad.tipo_prospeccion, id_proyecto, id_prospeccion, humedad.humedad, humedad.profundidad_promedio, humedad.area])

    wb.save(response)
    return response

#Exportar pdf (dentro de listar humedad)
def export_to_pdf_humedad(request):
    # Implementación de exportación a PDF
    return HttpResponse("Exportar a PDF no está implementado")


#ver humedad############################
def ver_humedad(request, pk):
    humedad = get_object_or_404(Humedad, pk=pk)
    return render(request, 'laboratorio/ensayos/humedad/ver_humedad.html', {'humedad': humedad})


#editar humedad############################
def editar_humedad(request, pk):
    humedad = get_object_or_404(Humedad, pk=pk)
    if request.method == 'POST':
        form = HumedadForm(request.POST, instance=humedad)
        if form.is_valid():
            form.save()
            return redirect('listar_humedad')
    else:
        form = HumedadForm(instance=humedad)
    return render(request, 'laboratorio/ensayos/humedad/editar_humedad.html', {'form': form})


#eliminar humedad############################
def eliminar_humedad(request, pk):
    humedad = get_object_or_404(Humedad, pk=pk)
    if request.method == 'POST':
        humedad.delete()
        return redirect('listar_humedad')
    return render(request, 'laboratorio/ensayos/humedad/eliminar_humedad.html', {'humedad': humedad})


#Grafico de humedad############################

# Obtener áreas
def obtener_areas(request):
    id_proyecto = request.GET.get('id_proyecto')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto).values('area').distinct()
    areas = [pros['area'] for pros in prospecciones if pros['area']]
    areas_dict = {area: area for area in areas}
    return JsonResponse(areas_dict)

def obtener_tipos_prospeccion(request):
    id_proyecto = request.GET.get('id_proyecto')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto).values('tipo_prospeccion').distinct()
    tipos_prospeccion = {pros['tipo_prospeccion']: pros['tipo_prospeccion'] for pros in prospecciones}
    return JsonResponse(tipos_prospeccion)

def obtener_areas(request):
    id_proyecto = request.GET.get('id_proyecto')
    prospecciones = Prospecciones.objects.filter(id_proyecto=id_proyecto).values('area').distinct()
    areas = [pros['area'] for pros in prospecciones if pros['area']]
    areas_dict = {area: area for area in areas}
    return JsonResponse(areas_dict)


# Generar gráfico de humedad por área
def generar_grafico_humedad_area(df):
    areas_unicas = df['area'].unique()
    colores = {area: np.random.rand(3,) for area in areas_unicas}

    plt.figure()
    for area in areas_unicas:
        datos_area = df[df['area'] == area]
        plt.scatter(
            datos_area['humedad'],
            datos_area['profundidad_promedio'],
            color=colores[area],
            s=100,
            label=area,
            marker='+'
        )

    plt.gca().xaxis.set_ticks_position("top")
    plt.gca().xaxis.set_label_position("top")
    plt.gca().invert_yaxis()
    plt.xlabel("Humedad (%)")
    plt.ylabel("Profundidad (m)")
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

import pandas as pd

def generar_grafico_humedad_prospeccion(df):
    # Convertir id_prospeccion a tipo string si es necesario
    df['id_prospeccion'] = df['id_prospeccion'].astype(str)
    
    # Crear una columna con el número secuencial para cada 'id_prospeccion'
    df['id_prospeccion_unico'] = df.groupby('id_prospeccion').cumcount() + 1
    
    # Crear la etiqueta con el formato 'id_prospeccion-id_unico'
    df['etiqueta'] = df['id_prospeccion'] + '-' + df['id_prospeccion_unico'].astype(str)
  
    prospecciones_unicas = df['etiqueta'].unique()  # Usamos la columna 'etiqueta'
    print("Valores únicos de 'etiqueta':", prospecciones_unicas)

    colores = {prospeccion: np.random.rand(3,) for prospeccion in prospecciones_unicas}

    plt.figure()
    for prospeccion in prospecciones_unicas:
        datos_prospeccion = df[df['etiqueta'] == prospeccion]
        plt.scatter(
            datos_prospeccion['humedad'],
            datos_prospeccion['profundidad_promedio'],
            color=colores[prospeccion],
            s=100,
            label=prospeccion,  # Usamos la etiqueta completa 'TPP-id_prospeccion-id_unico'
            marker='+'
        )

    plt.gca().xaxis.set_ticks_position("top")
    plt.gca().xaxis.set_label_position("top")
    plt.gca().invert_yaxis()
    plt.xlabel("Humedad (%)")
    plt.ylabel("Profundidad (m)")
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64


def graficos_humedad(request):
    proyectos = Proyectos.objects.all()
    prospecciones = Prospecciones.objects.all()
    areas = Humedad.objects.values_list('area', flat=True).distinct()
    humedades = Humedad.objects.all()

    id_proyecto = request.GET.getlist('id_proyecto')
    area = request.GET.get('area')

    if id_proyecto:
        humedades = humedades.filter(id_proyecto__in=id_proyecto)
    if area:
        humedades = humedades.filter(area__icontains=area)

    df = pd.DataFrame.from_records(humedades.values('id_proyecto', 'id_prospeccion', 'humedad', 'profundidad_promedio', 'area'))


    image_base64_area = generar_grafico_humedad_area(df) if not df.empty else None
    image_base64_prospeccion = generar_grafico_humedad_prospeccion(df) if not df.empty else None

    if image_base64_area and image_base64_prospeccion:
        return render(request, 'laboratorio/ensayos/humedad/graficos_humedad.html', {
            'image_base64_area': image_base64_area,
            'image_base64_prospeccion': image_base64_prospeccion,
            'proyectos': proyectos,
            'areas': areas
        })
    else:
        return JsonResponse({'error': 'No data available for the given filters.'})


from django.shortcuts import render

def indexx(request):
    return render(request, 'indexx.html')


############ENSAYOS LABORATORIO########################################

####DENSIDAD################################################

#Agregar densidad##############################################
#Listar densidad##############################################
#Ver densidad##############################################
#Editar densidad##############################################
#Eliminar densidad##############################################



############ENSAYOS LABORATORIO########################################

####SALES SOLUBLES TOTALES################################################


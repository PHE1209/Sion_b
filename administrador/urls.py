"""web_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views   #  <<==========
from .views import login_view, mi_vista_protegida, home_view, export_to_excel, export_to_pdf  # Importa las funciones necesarias
from django.contrib.auth.views import LogoutView  # Importa LogoutView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    
    path('', home_view, name="home"), # Redirige la raíz a la vista de inicio
    path('login', login_view, name='login'), # Inicio de Sesion
    path('index', mi_vista_protegida, name="index"), 
    path('', LogoutView.as_view(), name='logout'), # Agrega la URL de cierre de sesión
    path('indexx', views.indexx, name='indexx'), 
                
    path('listar_usuarios', views.listar_usuarios, name="listar_usuarios"),
    path('agregar_usuarios', views.agregar_usuarios, name="agregar_usuarios"),
    path('editar_usuarios', views.editar_usuarios, name="editar_usuarios"),
    path('eliminar_usuarios', views.eliminar_usuarios, name="eliminar_usuarios"),
  
    path('agregar_proyectos', views.agregar_proyectos, name="agregar_proyectos"),
    path('listar_proyectos', views.listar_proyectos, name="listar_proyectos"),
    path('ver_proyectos<int:n>', views.ver_proyectos, name='ver_proyectos'),
    path('editar_proyectos<int:n>', views.editar_proyectos, name='editar_proyectos'),
    path('eliminar_proyectos/<int:n>', views.eliminar_proyectos, name='eliminar_proyectos'),
    
    path('export/excel/', export_to_excel, name='export_to_excel'),
    path('export/pdf/', export_to_pdf, name='export_to_pdf'),
    
    path('agregar_prospecciones', views.agregar_prospecciones, name='agregar_prospecciones'),
    path('listar_prospecciones', views.listar_prospecciones, name='listar_prospecciones'),  
    path('obtener_tipos_prospeccion/', views.obtener_tipos_prospeccion, name='obtener_tipos_prospeccion'),
    path('obtener_id_prospecciones/', views.obtener_id_prospecciones, name='obtener_id_prospecciones'),
    path('get_area', views.get_area, name='get_area'),
    path('ver_prospeccion/<int:n>', views.ver_prospeccion, name='ver_prospeccion'),
    path('editar_prospeccion/<int:n>', views.editar_prospeccion, name='editar_prospeccion'),
    path('eliminar_prospeccion/<int:n>', views.eliminar_prospeccion, name='eliminar_prospeccion'),
    path('export_to_excel_prospecciones', views.export_to_excel_prospecciones, name='export_to_excel_prospecciones'),
    path('export_to_pdf_prospecciones', views.export_to_pdf_prospecciones, name='export_to_pdf_prospecciones'),

    path('agregar_muestreo', views.agregar_muestreo, name='agregar_muestreo'),
    path('listar_muestreo', views.listar_muestreo, name='listar_muestreo'),
    path('ver_muestreo/<int:n>', views.ver_muestreo, name='ver_muestreo'),
    path('editar_muestreo/<int:n>', views.editar_muestreo, name='editar_muestreo'),
    path('eliminar_muestreo/<int:pk>', views.eliminar_muestreo, name='eliminar_muestreo'),
    path('export_to_excel_muestreo', views.export_to_excel_muestreo, name='export_to_excel_muestreo'),
    path('export_to_pdf_muestreo', views.export_to_pdf_muestreo, name='export_to_pdf_muestreo'),


    path('agregar_humedad', views.agregar_humedad, name='agregar_humedad'),
    path('get_area/', views.get_area, name='get_area'),  # Nueva ruta para la solicitud AJAX
    path('listar_humedad', views.listar_humedad, name='listar_humedad'),
    path('export_to_excel_humedad/', views.export_to_excel_humedad, name='export_to_excel_humedad'),
    path('export_to_pdf_humedad/', views.export_to_pdf_humedad, name='export_to_pdf_humedad'),
    path('ver_humedad/<int:pk>/', views.ver_humedad, name='ver_humedad'),
    path('editar_humedad/<int:pk>/', views.editar_humedad, name='editar_humedad'),
    path('eliminar_humedad/<int:pk>/', views.eliminar_humedad, name='eliminar_humedad'),

    path('graficos_humedad', views.graficos_humedad, name='graficos_humedad'),
    path('obtener_areas/', views.obtener_areas, name='obtener_areas'),






]

    
    
    

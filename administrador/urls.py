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
from django.urls import path, include  # Importa include
from . import views
from .views import login_view, mi_vista_protegida, home_view, MiVistaProtegida, index_view
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', home_view, name="home"),
    path('login', login_view, name='login'),
    path('mi-vista-protegida', mi_vista_protegida, name="mi_vista_protegida"),
    path('otra-vista-protegida', MiVistaProtegida.as_view(), name="otra_vista_protegida"),
    path('logout', LogoutView.as_view(next_page='home'), name='logout'),
    path('index', index_view, name='index'),

    #Nomina y roster
    path('agregar_nomina', views.agregar_nomina, name='agregar_nomina'),
    path('listar_nomina', views.listar_nomina, name='listar_nomina'),
    path('editar_nomina/<int:id>', views.editar_nomina, name='editar_nomina'),
    path('ver_nomina/<int:id>/', views.ver_nomina, name='ver_nomina'),
    path('eliminar_nomina/<int:id>/', views.eliminar_nomina, name='eliminar_nomina'),
    path('export_to_excel_nomina', views.export_to_excel_nomina, name='export_to_excel_nomina'),
    path('export_to_pdf_nomina', views.export_to_pdf_nomina, name='export_to_pdf_nomina'),
    path('export_to_excel_roster', views.export_to_excel_roster, name='export_to_excel_roster'),
    path('export_to_pdf_roster', views.export_to_pdf_roster, name='export_to_pdf_roster'),
    path('listar_roster', views.listar_roster, name='listar_roster'),
    path('actualizar_hora/', views.actualizar_hora, name='actualizar_hora'), 

    #Proyectos
    path('agregar_proyectos', views.agregar_proyectos, name="agregar_proyectos"),
    path('listar_proyectos', views.listar_proyectos, name="listar_proyectos"),
    path('ver_proyectos/<str:id>', views.ver_proyectos, name='ver_proyectos'),
    path('editar_proyectos/<str:id>', views.editar_proyectos, name='editar_proyectos'),
    path('eliminar_proyectos/<str:id>', views.eliminar_proyectos, name='eliminar_proyectos'),
    path('export_to_excel_proyectos', views.export_to_excel_proyectos, name='export_to_excel_proyectos'),
    path('export_to_pdf_proyectos', views.export_to_pdf_proyectos, name='export_to_pdf_proyectos'),

    #Prospecciones
    path('agregar_prospecciones', views.agregar_prospecciones, name='agregar_prospecciones'),
    path('listar_prospecciones', views.listar_prospecciones, name='listar_prospecciones'),
    path('ver_prospecciones/<int:id>', views.ver_prospecciones, name='ver_prospecciones'),
    path('editar_prospecciones/<int:id>', views.editar_prospecciones, name='editar_prospecciones'),
    path('eliminar_prospecciones/<int:id>', views.eliminar_prospecciones, name='eliminar_prospecciones'),
    path('export_to_excel_prospecciones', views.export_to_excel_prospecciones, name='export_to_excel_prospecciones'),
    path('export_to_pdf_prospecciones', views.export_to_pdf_prospecciones, name='export_to_pdf_prospecciones'),
    path('graficos_prospecciones', views.graficos_prospecciones, name='graficos_prospecciones'),
    path('obtener_proyectos_prospecciones/', views.obtener_proyectos_prospecciones, name='obtener_proyectos_prospecciones'),
    path('eliminar_imagen/', views.eliminar_imagen, name='eliminar_imagen'),
    path('agregar_imagen/', views.agregar_imagen, name='agregar_imagen'),


    #Muestreo
    path('agregar_muestreo', views.agregar_muestreo, name='agregar_muestreo'),
    path('listar_muestreo', views.listar_muestreo, name='listar_muestreo'),
    path('editar_muestreo/<int:id>', views.editar_muestreo, name='editar_muestreo'),
    path('ver_muestreo/<int:id>', views.ver_muestreo, name='ver_muestreo'),
    path('eliminar_muestreo/<int:id>', views.eliminar_muestreo, name='eliminar_muestreo'),
    path('export_to_excel_muestreo/', views.export_to_excel_muestreo, name='export_to_excel_muestreo'),
    path('export_to_pdf_muestreo/', views.export_to_pdf_muestreo, name='export_to_pdf_muestreo'),
    path('graficos_muestreo', views.graficos_muestreo, name='graficos_muestreo'),
    path('obtener_tipos_prospeccion_muestreo', views.obtener_tipos_prospeccion_muestreo, name='obtener_tipos_prospeccion_muestreo'),
    path('obtener_id_prospecciones_muestreo', views.obtener_id_prospecciones_muestreo, name='obtener_id_prospecciones_muestreo'),
    path('obtener_area_muestreo', views.obtener_area_muestreo, name='obtener_area_muestreo'),
    path('agregar_imagen_muestreo/', views.agregar_imagen_muestreo, name='agregar_imagen_muestreo'),
    path('eliminar_imagen_muestreo/', views.eliminar_imagen_muestreo, name='eliminar_imagen_muestreo'),


    #Programa
    path('agregar_programa', views.agregar_programa, name='agregar_programa'),
    path('listar_programa', views.listar_programa, name='listar_programa'),
    path('ver_programa/<str:id>', views.ver_programa, name='ver_programa'),
    path('editar_programa/<str:id>/editar/', views.editar_programa, name='editar_programa'),
    path('eliminar_programa/<str:id>/eliminar/', views.eliminar_programa, name='eliminar_programa'),
    path('estatus_programa', views.estatus_programa, name='estatus_programa'),
    path('exportar_to_excel_programa/', views.export_to_excel_programa, name='export_to_excel_programa'),
    path('exportar_to_pdf_programa/', views.export_to_pdf_programa, name='export_to_pdf_programa'),

    #Humedad
    path('agregar_humedad', views.agregar_humedad, name='agregar_humedad'),
    path('listar_humedad', views.listar_humedad, name='listar_humedad'),
    path('editar_humedad/<int:id>', views.editar_humedad, name='editar_humedad'),
    path('ver_humedad/<int:id>', views.ver_humedad, name='ver_humedad'),
    path('eliminar_humedad/<int:id>', views.eliminar_humedad, name='eliminar_humedad'),
    path('export_to_excel_humedad/', views.export_to_excel_humedad, name='export_to_excel_humedad'),
    path('export_to_pdf_humedad/', views.export_to_pdf_humedad, name='export_to_pdf_humedad'),
    path('graficos_humedad', views.graficos_humedad, name='graficos_humedad'),
    path('obtener_tipos_prospeccion_humedad', views.obtener_tipos_prospeccion_humedad, name='obtener_tipos_prospeccion_humedad'),
    path('obtener_id_prospecciones_humedad', views.obtener_id_prospecciones_humedad, name='obtener_id_prospecciones_humedad'),
    path('obtener_area_humedad', views.obtener_area_humedad, name='obtener_area_humedad'),


    
    # USCS
    path('agregar_uscs', views.agregar_uscs, name='agregar_uscs'),
    path('listar_uscs', views.listar_uscs, name='listar_uscs'),
    path('editar_uscs/<str:id>', views.editar_uscs, name='editar_uscs'),
    path('ver_uscs/<int:id>', views.ver_uscs, name='ver_uscs'),
    path('eliminar_uscs/<str:id>/', views.eliminar_uscs, name='eliminar_uscs'),
    path('graficos_uscs', views.graficos_uscs, name='graficos_uscs'),
    path('export_to_excel_uscs/', views.export_to_excel_uscs, name='export_to_excel_uscs'), 
    path('export_to_pdf_uscs/', views.export_to_pdf_uscs, name='export_to_pdf_uscs'),     
    path('obtener_area_uscs', views.obtener_area_uscs, name='obtener_area_uscs'),


    # Gravedad Específica
    path('agregar_gravedad_especifica', views.agregar_gravedad_especifica, name='agregar_gravedad_especifica'),
    path('listar_gravedad_especifica', views.listar_gravedad_especifica, name='listar_gravedad_especifica'),
    path('editar_gravedad_especifica/<str:id>', views.editar_gravedad_especifica, name='editar_gravedad_especifica'),
    path('ver_gravedad_especifica/<int:id>', views.ver_gravedad_especifica, name='ver_gravedad_especifica'),
    path('eliminar_gravedad_especifica/<str:id>', views.eliminar_gravedad_especifica, name='eliminar_gravedad_especifica'),
    path('export_to_excel_gravedad_especifica/', views.export_to_excel_gravedad_especifica, name='export_to_excel_gravedad_especifica'),
    path('export_to_pdf_gravedad_especifica/', views.export_to_pdf_gravedad_especifica, name='export_to_pdf_gravedad_especifica'),
    path('graficos_gravedad_especifica', views.graficos_gravedad_especifica, name='graficos_gravedad_especifica'),
    path('obtener_tipos_prospeccion_gravedad', views.obtener_tipos_prospeccion_gravedad, name='obtener_tipos_prospeccion_gravedad'),
    path('obtener_id_prospecciones_gravedad', views.obtener_id_prospecciones_gravedad, name='obtener_id_prospecciones_gravedad'),
    path('obtener_area_gravedad', views.obtener_area_gravedad, name='obtener_area_gravedad'),


    # Límites de Atterberg
    path('agregar_limites_atterberg', views.agregar_limites_atterberg, name='agregar_limites_atterberg'),
    path('listar_limites_atterberg', views.listar_limites_atterberg, name='listar_limites_atterberg'),
    path('editar_limites_atterberg/<str:id>', views.editar_limites_atterberg, name='editar_limites_atterberg'),
    path('ver_limites_atterberg/<int:id>', views.ver_limites_atterberg, name='ver_limites_atterberg'),
    path('eliminar_limites_atterberg/<str:id>', views.eliminar_limites_atterberg, name='eliminar_limites_atterberg'),
    path('export_to_excel_limites_atterberg/', views.export_to_excel_limites_atterberg, name='export_to_excel_limites_atterberg'),
    path('export_to_pdf_limites_atterberg/', views.export_to_pdf_limites_atterberg, name='export_to_pdf_limites_atterberg'),
    path('graficos_limites_atterberg', views.graficos_limites_atterberg, name='graficos_limites_atterberg'),
    path('obtener_tipos_prospeccion_limites_atterberg', views.obtener_tipos_prospeccion_limites_atterberg, name='obtener_tipos_prospeccion_limites_atterberg'),
    path('obtener_id_prospecciones_limites_atterberg', views.obtener_id_prospecciones_limites_atterberg, name='obtener_id_prospecciones_limites_atterberg'),
    path('obtener_area_limites_atterberg', views.obtener_area_limites_atterberg, name='obtener_area_limites_atterberg'),

    #Granulometria    
    path('agregar_granulometria', views.agregar_granulometria, name='agregar_granulometria'),
    path('listar_granulometria', views.listar_granulometria, name='listar_granulometria'),
    path('editar_granulometria/<str:id>', views.editar_granulometria, name='editar_granulometria'),
    path('ver_granulometria/<int:id>', views.ver_granulometria, name='ver_granulometria'),
    path('eliminar_granulometria/<str:id>', views.eliminar_granulometria, name='eliminar_granulometria'),
    path('export_to_excel_granulometria/', views.export_to_excel_granulometria, name='export_to_excel_granulometria'),
    path('export_to_pdf_granulometria/', views.export_to_pdf_granulometria, name='export_to_pdf_granulometria'),
    path('graficos_granulometria', views.graficos_granulometria, name='graficos_granulometria'),
    path('obtener_tipos_prospeccion_granulometria', views.obtener_tipos_prospeccion_granulometria, name='obtener_tipos_prospeccion_granulometria'),
    path('obtener_id_prospecciones_granulometria', views.obtener_id_prospecciones_granulometria, name='obtener_id_prospecciones_granulometria'),
    path('obtener_area_granulometria', views.obtener_area_granulometria, name='obtener_area_granulometria'),
   

    # CBR
    path('agregar_cbr', views.agregar_cbr, name='agregar_cbr'),
    path('listar_cbr', views.listar_cbr, name='listar_cbr'),
    path('editar_cbr/<str:id>', views.editar_cbr, name='editar_cbr'),
    path('ver_cbr/<int:id>', views.ver_cbr, name='ver_cbr'),
    path('eliminar_cbr/<str:id>', views.eliminar_cbr, name='eliminar_cbr'),
    path('export_to_excel_cbr/', views.export_to_excel_cbr, name='export_to_excel_cbr'),
    path('export_to_pdf_cbr/', views.export_to_pdf_cbr, name='export_to_pdf_cbr'),
    path('graficos_cbr', views.graficos_cbr, name='graficos_cbr'),
    path('obtener_tipos_prospeccion_cbr', views.obtener_tipos_prospeccion_cbr, name='obtener_tipos_prospeccion_cbr'),
    path('obtener_id_prospecciones_cbr', views.obtener_id_prospecciones_cbr, name='obtener_id_prospecciones_cbr'),

    #Densidad Insitu
    path('agregar_densidad_insitu', views.agregar_densidad_insitu, name='agregar_densidad_insitu'),
    path('listar_densidad_insitu', views.listar_densidad_insitu, name='listar_densidad_insitu'),
    path('editar_densidad_insitu/<int:id>', views.editar_densidad_insitu, name='editar_densidad_insitu'),
    path('ver_densidad_insitu/<int:id>', views.ver_densidad_insitu, name='ver_densidad_insitu'),
    path('eliminar_densidad_insitu/<int:id>', views.eliminar_densidad_insitu, name='eliminar_densidad_insitu'),
    path('export_to_excel_densidad_insitu/', views.export_to_excel_densidad_insitu, name='export_to_excel_densidad_insitu'),
    path('export_to_pdf_densidad_insitu/', views.export_to_pdf_densidad_insitu, name='export_to_pdf_densidad_insitu'),
    path('graficos_densidad_insitu', views.graficos_densidad_insitu, name='graficos_densidad_insitu'),
    path('obtener_tipos_prospeccion_densidad_insitu', views.obtener_tipos_prospeccion_densidad_insitu, name='obtener_tipos_prospeccion_densidad_insitu'),
    path('obtener_id_prospecciones_densidad_insitu', views.obtener_id_prospecciones_densidad_insitu, name='obtener_id_prospecciones_densidad_insitu'),
    path('obtener_area_densidad_insitu', views.obtener_area_densidad_insitu, name='obtener_area_densidad_insitu'),


    #Tranversal
    path('obtener_proyectos_prospecciones/', views.obtener_proyectos_prospecciones, name='obtener_proyectos_prospecciones'),
    path('obtener_tipos_prospeccion', views.obtener_tipos_prospeccion, name='obtener_tipos_prospeccion'),
    path('obtener_id_prospecciones/', views.obtener_id_prospecciones, name='obtener_id_prospecciones'),
    #path('get_area', views.get_area, name='get_area'),

   
    path('historial', views.historial, name='historial'), 
    

   path('docs/', views.docs_view, name='docs'),  # Ruta para "/docs"


]

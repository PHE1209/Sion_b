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

    #Muestreo
    path('agregar_muestreo', views.agregar_muestreo, name='agregar_muestreo'),
    path('listar_muestreo', views.listar_muestreo, name='listar_muestreo'),
    path('ver_muestreo/<str:id>', views.ver_muestreo, name='ver_muestreo'),
    path('editar_muestreo/<str:id>', views.editar_muestreo, name='editar_muestreo'),
    path('eliminar_muestreo/<str:id>', views.eliminar_muestreo, name='eliminar_muestreo'),
    path('export_to_excel_muestreo', views.export_to_excel_muestreo, name='export_to_excel_muestreo'),
    path('export_to_pdf_muestreo', views.export_to_pdf_muestreo, name='export_to_pdf_muestreo'),

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
    path('ver_humedad/<str:id>/', views.ver_humedad, name='ver_humedad'),
    path('editar_humedad/<str:id>', views.editar_humedad, name='editar_humedad'),
    path('eliminar_humedad/<str:id>/', views.eliminar_humedad, name='eliminar_humedad'),
    path('export_to_excel_humedad/', views.export_to_excel_humedad, name='export_to_excel_humedad'),
    path('export_to_pdf_humedad/', views.export_to_pdf_humedad, name='export_to_pdf_humedad'),
    path('graficos_humedad', views.graficos_humedad, name='graficos_humedad'),    
    path('obtener_id_proyecto_humedad', views.obtener_id_proyecto_humedad, name='obtener_id_proyecto_humedad'),
    path('obtener_tipos_prospeccion_humedad', views.obtener_tipos_prospeccion_humedad, name='obtener_tipos_prospeccion_humedad'),
    path('obtener_id_prospecciones_humedad', views.obtener_id_prospecciones_humedad, name='obtener_id_prospecciones_humedad'),
    path('obtener_areas_humedad', views.obtener_areas_humedad, name='obtener_areas_humedad'),


    #Granulometria    
    path('agregar_granulometria', views.agregar_granulometria, name='agregar_granulometria'),
    path('listar_granulometria', views.listar_granulometria, name='listar_granulometria'),
    path('ver_granulometria/<str:id>', views.ver_granulometria, name='ver_granulometria'),
    path('editar_granulometria/<str:id>', views.editar_granulometria, name='editar_granulometria'),
    path('eliminar_granulometria/<str:id>/', views.eliminar_granulometria, name='eliminar_granulometria'),
    path('export_to_excel_granulometria/', views.export_to_excel_granulometria, name='export_to_excel_granulometria'),
    path('export_to_pdf_granulometria/', views.export_to_pdf_granulometria, name='export_to_pdf_granulometria'),
    path('graficos_granulometria', views.graficos_granulometria, name='graficos_granulometria'),  
    path('api/proyectos', views.obtener_id_proyecto_granulometria, name='obtener_id_proyecto'),    
    path('api/tipos-prospeccion', views.obtener_tipos_prospeccion_granulometria, name='obtener_tipos_prospeccion'),
    path('api/id-prospecciones', views.obtener_id_prospecciones_granulometria, name='obtener_id_prospecciones'),
    path('api/areas', views.obtener_areas_granulometria, name='obtener_areas'),
    
    
    # USCS
    path('agregar_uscs', views.agregar_uscs, name='agregar_uscs'),
    path('listar_uscs', views.listar_uscs, name='listar_uscs'),
    path('editar_uscs/<str:id>', views.editar_uscs, name='editar_uscs'),
    path('ver_uscs/<int:id>/', views.ver_uscs, name='ver_uscs'),
    path('eliminar_uscs/<str:id>/', views.eliminar_uscs, name='eliminar_uscs'),
    path('graficos_uscs', views.graficos_uscs, name='graficos_uscs'),
    path('export_to_excel_uscs/', views.export_to_excel_uscs, name='export_to_excel_uscs'),  # Si deseas exportación
    path('export_to_pdf_uscs/', views.export_to_pdf_uscs, name='export_to_pdf_uscs'),      # Si deseas exportación


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

    


    #Tranversal
    path('obtener_proyectos_prospecciones/', views.obtener_proyectos_prospecciones, name='obtener_proyectos_prospecciones'),
    path('obtener_tipos_prospeccion', views.obtener_tipos_prospeccion, name='obtener_tipos_prospeccion'),
    path('obtener_id_prospecciones/', views.obtener_id_prospecciones, name='obtener_id_prospecciones'),
    path('get_area', views.get_area, name='get_area'),

   
    path('historial', views.historial, name='historial'), 
    
    
    # URLs AJAX (compartidas con uscs, gravedad especifica, )
    path('agregar_uscs/', views.agregar_uscs, name='agregar_uscs'),
    path('obtener_tipos_prospeccion_muestreo/', views.obtener_tipos_prospeccion_muestreo, name='obtener_tipos_prospeccion_muestreo'),
    path('obtener_id_prospecciones_muestreo/', views.obtener_id_prospecciones_muestreo, name='obtener_id_prospecciones_muestreo'),
    path('obtener_area_muestreo/', views.obtener_area_muestreo, name='obtener_area_muestreo'),
    path('obtener_id_muestras_muestreo/', views.obtener_id_muestras_muestreo, name='obtener_id_muestras_muestreo'),
    path('obtener_profundidades_muestreo/', views.obtener_profundidades_muestreo, name='obtener_profundidades_muestreo'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

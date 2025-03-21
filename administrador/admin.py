from django.contrib import admin

# Register your models here.

from .models import Poll ,Choice , Nomina, Proyectos, Prospecciones, Humedad, Muestreo

admin.site.register(Poll )
admin.site.register(Choice )
admin.site.register(Nomina )
admin.site.register(Proyectos )
admin.site.register(Prospecciones )
admin.site.register(Humedad )
admin.site.register(Muestreo )

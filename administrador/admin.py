from django.contrib import admin

# Register your models here.

from .models import Poll ,Choice , Usuarios, Proyectos, Prospecciones, Humedad

admin.site.register(Poll )
admin.site.register(Choice )
admin.site.register(Usuarios )
admin.site.register(Proyectos )
admin.site.register(Prospecciones )
admin.site.register(Humedad )

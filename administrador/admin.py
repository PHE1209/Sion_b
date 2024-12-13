from django.contrib import admin

# Register your models here.

from .models import Poll ,Choice , Usuarios, Proyectos

admin.site.register(Poll )
admin.site.register(Choice )
admin.site.register(Usuarios )
admin.site.register(Proyectos )

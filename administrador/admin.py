from django.contrib import admin

# Register your models here.

from .models import Poll ,Choice , usuarios, proyectos

admin.site.register(Poll )
admin.site.register(Choice )
admin.site.register(usuarios )
admin.site.register(proyectos )

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
"""
web_admin URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from administrador.views import home_view  # Importamos home_view directamente

def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrador/', include('administrador.urls')),
    path('', home_view, name='home'),  # Usamos home_view para la raíz
    path('health/', health_check, name='health_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
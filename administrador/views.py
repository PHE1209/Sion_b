from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Usuarios # Se separan por comas a medida que se van agregando mas tablas


# Create your views here.

TEMPLATE_DIR = (
    'os.path.join(BASE_DIR, "templates),'
)

## crear nuevo registros
def index(request):                    #  <<==========
    return render(request,"index.html")      #  <<==========

def listar(request):
    users = Usuarios.objects.all()
    datos = {'usuarios' : users}
    return render(request, "usuarios/listar.html", datos)


## agregar
def agregar(request):
    if request.method=='POST':
       if request.POST.get('empresa') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('email') and request.POST.get('telefono'):
        u = Usuarios()
        u.empresa = request.POST.get('empresa')
        u.nombre = request.POST.get('nombre')
        u.apellido = request.POST.get('apellido')
        u.email = request.POST.get('email')
        u.telefono = request.POST.get('telefono')
        u.save()
        return redirect('listar')
    else:
        return render(request, "usuarios/agregar.html")

## actualizar registros
def actualizar(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        if user_id and all(key in request.POST for key in ['empresa', 'nombre', 'apellido', 'email', 'telefono']):
            u = get_object_or_404(Usuarios, id=user_id)
            u.empresa = request.POST.get('empresa')
            u.nombre = request.POST.get('nombre')
            u.apellido = request.POST.get('apellido')
            u.email = request.POST.get('email')
            u.telefono = request.POST.get('telefono')
            u.save()
            return redirect('listar')
    else:
        usuarios = Usuarios.objects.all()
        return render(request, "usuarios/actualizar.html", {'usuarios': usuarios})

    usuarios = Usuarios.objects.all()
    return render(request, "usuarios/actualizar.html", {'usuarios': usuarios})

## eliminar registros
def eliminar(request):
    if request.method == 'POST':
        if request.POST.get('id'):
            id_a_borrar = request.POST.get('id')
            registro = get_object_or_404(Usuarios, id=id_a_borrar)
            registro.delete()
            return redirect('listar')
    else:
        usuarios = Usuarios.objects.all()
        datos = {'usuarios': usuarios}
        return render(request, "usuarios/eliminar.html", datos)

    return render(request, "usuarios/eliminar.html", datos)


    
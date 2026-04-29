from django.shortcuts import render, redirect
from .models import Plato, Reserva


def index(request):
    platos_destacados = Plato.objects.filter(disponible=True)[:3]
    return render(request, 'catering/index.html', {'platos': platos_destacados})


def menu(request):
    categorias = ['entrada', 'principal', 'postre', 'bebida']
    menu_por_categoria = {
        cat: Plato.objects.filter(categoria=cat, disponible=True)
        for cat in categorias
    }
    return render(request, 'catering/menu.html', {'menu': menu_por_categoria})


def contacto(request):
    if request.method == 'POST':
        Reserva.objects.create(
            nombre_cliente    = request.POST['nombre'],
            email             = request.POST['email'],
            telefono          = request.POST['telefono'],
            fecha_evento      = request.POST['fecha'],
            cantidad_personas = request.POST['personas'],
            mensaje           = request.POST.get('mensaje', '')
        )
        return redirect('index')
    return render(request, 'catering/contacto.html')
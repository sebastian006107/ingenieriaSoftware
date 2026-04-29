from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Habitacion, Reserva
from datetime import date

def inicio(request):
    habitaciones = Habitacion.objects.filter(disponible=True)[:3]
    return render(request, 'inicio.html', {'habitaciones': habitaciones})

def login_view(request):
    if request.method == 'POST':
        rut = request.POST['rut']
        password = request.POST['password']
        user = authenticate(request, rut=rut, password=password)
        if user:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'RUT o clave incorrectos')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def catalogo(request):
    habitaciones = Habitacion.objects.filter(disponible=True)
    categoria = request.GET.get('categoria')
    if categoria:
        habitaciones = habitaciones.filter(categoria=categoria)
    return render(request, 'catalogo.html', {'habitaciones': habitaciones})

def detalle_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    return render(request, 'detalle.html', {'habitacion': habitacion})

@login_required
def reservar(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    if request.method == 'POST':
        fecha_entrada = request.POST['fecha_entrada']
        fecha_salida = request.POST['fecha_salida']
        
        from datetime import date, datetime
        entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
        salida = datetime.strptime(fecha_salida, '%Y-%m-%d').date()
        dias = (salida - entrada).days

        # Validar fechas
        if salida <= entrada:
            messages.error(request, 'La fecha de salida debe ser posterior a la entrada')
            return render(request, 'reservar.html', {'habitacion': habitacion})

        if dias < 3 or dias > 12:
            messages.error(request, 'La estadía debe ser entre 3 y 12 días')
            return render(request, 'reservar.html', {'habitacion': habitacion})

        # Verificar disponibilidad
        reservas_existentes = Reserva.objects.filter(
            habitacion=habitacion,
            fecha_entrada__lt=salida,
            fecha_salida__gt=entrada,
            estado__in=['pendiente', 'confirmada']
        )
        if reservas_existentes.exists():
            messages.error(request, 'La habitación no está disponible para esas fechas')
            return render(request, 'reservar.html', {'habitacion': habitacion})

        # Crear reserva
        reserva = Reserva(
            usuario=request.user,
            habitacion=habitacion,
            fecha_entrada=entrada,
            fecha_salida=salida,
        )
        reserva.calcular_montos()
        reserva.save()
        return redirect('confirmacion', id=reserva.id)

    return render(request, 'reservar.html', {'habitacion': habitacion})

@login_required
def confirmacion(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    return render(request, 'confirmacion.html', {'reserva': reserva})
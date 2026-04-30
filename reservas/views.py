from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Habitacion, Reserva, Usuario, ImagenHabitacion

def inicio(request):
    habitaciones = Habitacion.objects.filter(disponible=True)[:3]
    return render(request, 'inicio.html', {'habitaciones': habitaciones})

def registro_view(request):
    if request.method == 'POST':
        rut = request.POST['rut']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        password = request.POST['password']

        if Usuario.objects.filter(rut=rut).exists():
            messages.error(request, 'El RUT ya está registrado')
            return render(request, 'registro.html')

        user = Usuario.objects.create_user(
            username=rut,
            rut=rut,
            first_name=nombre,
            last_name=apellido,
            email=email,
            password=password,
        )
        login(request, user)
        return redirect('inicio')

    return render(request, 'registro.html')




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
    capacidad = request.GET.get('capacidad')
    if categoria:
        habitaciones = habitaciones.filter(categoria=categoria)
    if capacidad:
        cap = int(capacidad)
        if cap >= 3:
            habitaciones = habitaciones.filter(capacidad__gte=3)
        else:
            habitaciones = habitaciones.filter(capacidad=cap)
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

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'mis_reservas.html', {'reservas': reservas})



from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/login/')
def admin_dashboard(request):
    from django.utils import timezone
    total_reservas = Reserva.objects.count()
    reservas_hoy = Reserva.objects.filter(fecha_creacion__date=timezone.now().date()).count()
    total_habitaciones = Habitacion.objects.count()
    habitaciones_disponibles = Habitacion.objects.filter(disponible=True).count()
    ocupacion = round((total_habitaciones - habitaciones_disponibles) / max(total_habitaciones, 1) * 100)
    reservas_recientes = Reserva.objects.select_related('usuario', 'habitacion').order_by('-fecha_creacion')[:10]

    context = {
        'total_reservas': total_reservas,
        'reservas_hoy': reservas_hoy,
        'habitaciones_disponibles': habitaciones_disponibles,
        'ocupacion': ocupacion,
        'reservas_recientes': reservas_recientes,
    }
    return render(request, 'admin_dashboard.html', context)

@staff_member_required(login_url='/login/')
def admin_cancelar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.estado = 'cancelada'
    reserva.save()
    return redirect('admin_reservas')



@staff_member_required(login_url='/login/')
def admin_reservas(request):
    reservas = Reserva.objects.select_related('usuario', 'habitacion').order_by('-fecha_creacion')
    estado = request.GET.get('estado')
    if estado:
        reservas = reservas.filter(estado=estado)
    return render(request, 'admin_reservas.html', {'reservas': reservas, 'estado_actual': estado})

@staff_member_required(login_url='/login/')
def admin_modificar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    if request.method == 'POST':
        fecha_entrada = request.POST['fecha_entrada']
        fecha_salida = request.POST['fecha_salida']
        from datetime import datetime
        entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
        salida = datetime.strptime(fecha_salida, '%Y-%m-%d').date()
        dias = (salida - entrada).days
        if salida <= entrada:
            messages.error(request, 'La fecha de salida debe ser posterior a la entrada')
            return render(request, 'admin_modificar_reserva.html', {'reserva': reserva})
        if dias < 3 or dias > 12:
            messages.error(request, 'La estadía debe ser entre 3 y 12 días')
            return render(request, 'admin_modificar_reserva.html', {'reserva': reserva})
        reserva.fecha_entrada = entrada
        reserva.fecha_salida = salida
        reserva.calcular_montos()
        reserva.save()
        messages.success(request, 'Reserva modificada correctamente')
        return redirect('admin_reservas')
    return render(request, 'admin_modificar_reserva.html', {'reserva': reserva})


@staff_member_required(login_url='/login/')
def admin_habitaciones(request):
    habitaciones = Habitacion.objects.all().order_by('numero')
    return render(request, 'admin_habitaciones.html', {'habitaciones': habitaciones})

@staff_member_required(login_url='/login/')
def admin_editar_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    if request.method == 'POST':
        habitacion.numero = request.POST['numero']
        habitacion.piso = request.POST['piso']
        habitacion.categoria = request.POST['categoria']
        habitacion.capacidad = request.POST['capacidad']
        habitacion.precio_noche = request.POST['precio_noche']
        habitacion.descripcion = request.POST['descripcion']
        habitacion.disponible = 'disponible' in request.POST
        habitacion.save()
        messages.success(request, 'Habitación actualizada correctamente')
        return redirect('admin_habitaciones')
    return render(request, 'admin_editar_habitacion.html', {'habitacion': habitacion})


@staff_member_required(login_url='/login/')
def admin_subir_imagen(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        descripcion = request.POST.get('descripcion', '')
        if imagen:
            ImagenHabitacion.objects.create(
                habitacion=habitacion,
                imagen=imagen,
                descripcion=descripcion
            )
            messages.success(request, 'Imagen subida correctamente')
        return redirect('admin_subir_imagen', id=id)
    imagenes = habitacion.imagenes.all()
    return render(request, 'admin_subir_imagen.html', {'habitacion': habitacion, 'imagenes': imagenes})

@staff_member_required(login_url='/login/')
def admin_eliminar_imagen(request, id):
    imagen = get_object_or_404(ImagenHabitacion, id=id)
    habitacion_id = imagen.habitacion.id
    imagen.imagen.delete()
    imagen.delete()
    return redirect('admin_subir_imagen', id=habitacion_id)
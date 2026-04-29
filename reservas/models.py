from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    rol = models.CharField(max_length=20, choices=[
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador'),
        ('admin', 'Administrador'),
    ], default='cliente')

    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return f"{self.get_full_name()} ({self.rut})"

class Habitacion(models.Model):
    CATEGORIA_CHOICES = [
        ('turista', 'Turista'),
        ('premium', 'Premium'),
    ]
    numero = models.IntegerField(unique=True)
    piso = models.IntegerField()
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES)
    capacidad = models.IntegerField()
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Habitación {self.numero} - Piso {self.piso} ({self.categoria})"

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    total_estadía = models.DecimalField(max_digits=10, decimal_places=2)
    monto_reserva = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pendiente = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def calcular_montos(self):
        from decimal import Decimal
        dias = (self.fecha_salida - self.fecha_entrada).days
        self.total_estadía = self.habitacion.precio_noche * dias
        self.monto_reserva = self.total_estadía * Decimal('0.30')
        self.monto_pendiente = self.total_estadía * Decimal('0.70')

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario} - Hab {self.habitacion.numero}"

from decimal import Decimal

def calcular_montos(self):
    dias = (self.fecha_salida - self.fecha_entrada).days
    self.total_estadía = self.habitacion.precio_noche * dias
    self.monto_reserva = self.total_estadía * Decimal('0.30')
    self.monto_pendiente = self.total_estadía * Decimal('0.70')

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario} - Hab {self.habitacion.numero}"
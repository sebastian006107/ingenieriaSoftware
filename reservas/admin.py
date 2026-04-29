from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Habitacion, Reserva

admin.site.register(Usuario, UserAdmin)
admin.site.register(Habitacion)
admin.site.register(Reserva)
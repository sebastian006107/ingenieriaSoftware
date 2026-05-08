from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Habitacion, Reserva, ImagenHabitacion

admin.site.register(Usuario, UserAdmin)
admin.site.register(Habitacion)
admin.site.register(Reserva)


@admin.register(ImagenHabitacion)
class ImagenHabitacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'habitacion', 'descripcion', 'orden')
    list_filter = ('habitacion', 'orden')
    search_fields = ('habitacion__numero', 'descripcion')
    ordering = ('habitacion', 'orden')
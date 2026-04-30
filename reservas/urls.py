from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('habitacion/<int:id>/', views.detalle_habitacion, name='detalle_habitacion'),
    path('reservar/<int:id>/', views.reservar, name='reservar'),
    path('confirmacion/<int:id>/', views.confirmacion, name='confirmacion'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/cancelar/<int:id>/', views.admin_cancelar_reserva, name='admin_cancelar_reserva'),
    path('admin-panel/reservas/', views.admin_reservas, name='admin_reservas'),
    path('admin-panel/reservas/modificar/<int:id>/', views.admin_modificar_reserva, name='admin_modificar_reserva'),
    path('admin-panel/habitaciones/', views.admin_habitaciones, name='admin_habitaciones'),
    path('admin-panel/habitaciones/editar/<int:id>/', views.admin_editar_habitacion, name='admin_editar_habitacion'),
    path('admin-panel/habitaciones/imagenes/<int:id>/', views.admin_subir_imagen, name='admin_subir_imagen'),
    path('admin-panel/habitaciones/imagenes/eliminar/<int:id>/', views.admin_eliminar_imagen, name='admin_eliminar_imagen'),

]
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
    
]
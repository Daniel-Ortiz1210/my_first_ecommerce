from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('agregar', views.add_to_cart, name='add'),
    path('eliminar', views.remove_from_cart, name='remove')
]
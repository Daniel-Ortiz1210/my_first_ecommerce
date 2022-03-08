from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='productos'),
    # debemos usar <pk> (primary key) obligatoriamente para visitar registros por id
    # si usamos slugs, debemos usar <slug:slug>
    path('buscar', views.product_search_view, name='search_view'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product'),
]
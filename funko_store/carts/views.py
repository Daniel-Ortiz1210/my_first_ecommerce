from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Cart
from .utils import get_or_create_cart
from products.models import Product
from .models import CartProducts
# Create your views here.

def cart(request):
    cart = get_or_create_cart(request)
    subtotal = cart.subtotal
    total = cart.total
    n_products = cart.products.all().count()
    product_quantities = cart.cartproducts_set.all()
    
    return render(request, 'carts/cart.html', {
        'cart': cart,
        'subtotal': subtotal,
        'total': total,
        'n_products': n_products,
        'product_quantities': product_quantities    
    })  

def add_to_cart(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1)) # En el cso que la llave no exista, asignamos 1
    
    # Añadir un producto a la relación con carrito - relacion muchos a muchos
    # cart.products.add(product, through_defaults={
    #     'quantity': quantity
    # })

    cart_product = CartProducts.objects.create_or_update_quantity(cart=cart, product=product, quantity=quantity)
    
    if quantity > 1:
        message = 'Productos agregados al carrito'
    else:
        message = 'Producto agregado al carrito'

    return render(request, 'add.html', {
        'product': product,
        'message': message
    })

def remove_from_cart(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    # Eliminar un producto de la relación con el carrito
    cart.products.remove(product)
    return redirect('cart')

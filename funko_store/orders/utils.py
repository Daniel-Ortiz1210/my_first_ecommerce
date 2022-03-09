from django.contrib import messages
from django.shortcuts import redirect
from .models import Order
from django.urls import reverse

def get_or_create_order(cart, request):
    user = request.user if request.user.is_authenticated else None
    order = cart.order

    if cart.products is None:
        messages.info(request, 'No tienes una orden de compra actualmente, agrega productos a tu carrito para generar una.')
        return redirect('index')

    if order is None:
        order = Order.objects.create(user=user, cart=cart)
    
    if user and order.user is None:
        order.user = user
        order.save()
    
    request.session['order_id'] = order.order_id
    return order

def breadcrumb(products=True, shipping=False, payment=False, confirmation=False):
    return [
        {'title': 'Productos', 'active':products, 'url':reverse('order')},
        {'title': 'Envío', 'active':shipping, 'url':reverse('order')},
        {'title': 'Pago', 'active':payment, 'url':reverse('order')},
        {'title': 'Confirmación', 'active':confirmation, 'url':reverse('order')},
        
    ]
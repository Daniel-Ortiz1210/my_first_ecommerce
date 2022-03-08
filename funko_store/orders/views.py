from django.shortcuts import render
from .utils import get_or_create_order
from carts.utils import get_or_create_cart
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def order(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    return render(request, 'orders/order.html', {
        'cart_products': cart.products.all(),
        'cart': cart,
        'order': order,
    })

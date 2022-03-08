from django.shortcuts import redirect, render
from .models import Product
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from.forms import SearchForm
# Create your views here.


def index(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'index.html', {
        'products': products
    })


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'

def product_search_view(request):
    print(request.GET.get('q'))
    products = Product.objects.filter(title__icontains=request.GET.get('q'))
    q = request.GET.get('q')
    n = products.count()
    return render(request, 'products/search-view.html', {
        'products': products,
        'q': q,
        'n': n
    })
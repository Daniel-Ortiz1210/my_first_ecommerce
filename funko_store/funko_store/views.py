from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout # con authenticate verificamos si el usuario existe en DB y con login iniciamos sesion con el usuario
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from customers.models import User
from products.models import Product

# username: danielop
# password: dex122706


def index(request):
    return redirect('productos/')
    # products = Product.objects.all().order_by('-id')
    # return render(request, 'index.html', {
    #     'products': products
    # })


def login_view(request):
    if request.user.is_authenticated:
        '''
        Si el usuario ya se esta autenticado, no tiene caso visitar esta url, lo redirijimos a index
        '''
        return redirect('index')

    form = LoginForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}')
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect('index')
        else:
            messages.error(request, 'No existe un usuario registrado con este username')
            return redirect('login')
    return render(request, 'login.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada con éxito!')
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        '''
        Si el usuario ya se esta autenticado, no tiene caso visitar esta url, lo redirijimos a index
        '''
        return redirect('index')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        '''
        Usamos el método .save() del fomulario de registro para crear el modelo del un usuario,
        porteriormente lo instanciamos como user
        '''
        # username = form.cleaned_data.get('username')
        # email = form.cleaned_data.get('email')
        # password = form.cleaned_data.get('password')
        user = form.save()
        if user is not None:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')
        else:
            messages.error(request, 'No pudimos crear el usuario')
            return redirect('register')
    return render(request, 'register.html', {
        'form': form
    })
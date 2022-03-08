from distutils.command.upload import upload
from turtle import title
from django.db import models

# Create your models here.


# Steps for activate models
# 1: Crear modelos
# 2: Añadir la app al archivo setting del proyecto
# 3: Registrar el modelo en admin.py con admin.site.register([model name])
# 4: ejecutar en terminal: python manage.py makemigrations [app_name]
# 5: ejecutar en terminal python manage.py migrate

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to='products/', null=True, blank=False)
    slug = models.SlugField(null=False, blank=False, unique=False, default='funko-pop')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''
        Mostrar el nombre original del producto en el administrador de Django 
        '''
        return self.title


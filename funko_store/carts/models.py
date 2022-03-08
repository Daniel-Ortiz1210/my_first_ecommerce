import decimal
import uuid
from django.db import models
from customers.models import User
from products.models import Product
from django.db.models.signals import pre_save, m2m_changed, post_save

# Create your models here.
class Cart(models.Model):
    '''
    user -> un usuario puede tener muchos carritos
    productos -> un producto puede tener muchos carritos, y un carrito puede tener muchos productos
    '''
    cart_id = models.CharField(max_length=100, null=True, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) # Uno a muchos
    products = models.ManyToManyField(Product, through='CartProducts')
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    FEE = 0.05

    def __str__(self) -> str:
        return f'{self.cart_id}'
    
    def update_totals(self):
        self.update_subtotal()
        self.update_total()

        order = self.order_set.first()
        if order:
            order.update_total()
            
    
    def update_subtotal(self):
        self.subtotal = sum(
            [ 
                cp.quantity * cp.product.price for cp in self.cartproducts_set.all()
            ]
        )

    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE) )
        self.save()

# -------------------------------------------------------------------------------------------
# IMPLEMENTACIÓN DEL MODELO
# Se debe primero eliminar las migraciones y la db, ya es un cambio grande, hacer respaldo de información

# 1 -> Creación del modelo
# 2 -> Hacer las migraciones sin establecer relaciones
# 3 -> Establecer las migraciones usando el atributo through, indicando a que modelo será relacionado
# 4 -> Volver a realizar las migraciones 
# 5 -> Aplicar las migraciones

# Actualizar un registro cada que agreguemos una nueva cantidada uno ya existente
class CardProductsManager(models.Manager):

    def create_or_update_quantity(self, cart, product, quantity=1):
        '''
        Obtener o crear un objeto segun ciertos parametros
        '''
        object, created = self.get_or_create(cart=cart, product=product)

        if not created:
            quantity =  object.quantity + quantity
        
        object.update_quantity(quantity)
        return object

# -----------------------------------------------------------------------------------------------------------


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CardProductsManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()


def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def post_save_totals(sender, instance, *args, **kwargs):
    instance.cart.update_totals()

def totals_signal(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.update_totals()

pre_save.connect(set_cart_id, sender=Cart)
post_save.connect(post_save_totals, sender=CartProducts)
m2m_changed.connect(totals_signal, sender=Cart.products.through)



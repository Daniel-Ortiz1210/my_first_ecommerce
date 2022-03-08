from random import choices
from django.db import models
from customers.models import User
from carts.models import Cart
from enum import Enum
import uuid
from django.db.models.signals import pre_save
import decimal



# Create your models here.
class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAID = 'PAID'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

choices = [(tag, tag.value) for tag in OrderStatus ]


class Order(models.Model):
    order_id = models.CharField(max_length=100, null=True, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=choices)
    shipping = models.DecimalField(max_digits=8, default=5, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.user.username}'

    def calculate_total(self):
        self.total = self.cart.total + self.shipping

    def update_total(self):
        self.total = self.calculate_total()
        self.save()

def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.calculate_total()

pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)
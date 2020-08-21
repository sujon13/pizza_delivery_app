from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .user_manager import UserManager


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=100)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    address = models.CharField(max_length=200, blank=True, default='')
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    lat = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name + ' ' + str(self.email) + ' ' + str(self.phone)


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, default='regular')
    availability = models.BooleanField(default=True)
    price = models.FloatField(verbose_name='price in TK')
    weight = models.FloatField(verbose_name='weight in ounces')
    image = models.ImageField(upload_to='shops/', blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name + ' (from ' + self.brand + ' brand) price: (' +\
               str(self.price) + ') weight: (' + str(self.weight) + ')'

    class Meta:
        indexes = [
            models.Index(fields=['name', 'price',]),
        ]


class Order(models.Model):
    ORDER_STATE = [
        ('submitted', 'Submitted'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
    ]

    pizza = models.ForeignKey(
        Pizza,
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    order_price = models.FloatField(
        verbose_name='order price in TK',
        help_text='quantity multiplied by unit price when ordered',
        blank=True
    )
    address = models.CharField(max_length=200, blank=True, default='')
    lat = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    order_state = models.CharField(max_length=15, choices=ORDER_STATE, default=ORDER_STATE[0][0])
    delivery_time = models.DateTimeField(help_text='THe time of delivery specified by store manager', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.order_price = self.pizza.price * self.quantity
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return 'pizza_name: ( ' + self.pizza.name + ') c_name: (' + str(self.customer.phone) + ') price: ' +\
               str(self.order_price)

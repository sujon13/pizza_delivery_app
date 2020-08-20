from django.contrib import admin
from .models import Pizza, Order, CustomUser

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Pizza)
admin.site.register(Order)
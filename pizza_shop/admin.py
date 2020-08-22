from django.contrib import admin
from .models import Pizza, Order, CustomUser


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'email', 'phone', 'address', 'image', 'lat', 'lng']}),
        ('Default information', {'fields': ['password', 'is_superuser', 'last_login', 'date_joined', 'user_permissions']}),
    ]

    list_display = ('name', 'email', 'phone')
    list_filter = ['name', 'phone']


class PizzaAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'weight']
    list_filter = ['name', 'brand']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'pizza', 'quantity', 'order_price', 'order_state']


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Order, OrderAdmin)

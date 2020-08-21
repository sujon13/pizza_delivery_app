from .models import Pizza, Order, CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone', 'address', 'image', 'lat', 'lng']


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        exclude = ['tags']


class OrderPacingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_customer(self, value):
        """
        Check that customer is the current logged in user.
        """
        if self.context.get('user') != value:
            raise serializers.ValidationError("customer id is different from current logged in user")
        return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1

from .models import Pizza, Order, CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    #snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'phone', 'address', 'photo', 'lat', 'lng']


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

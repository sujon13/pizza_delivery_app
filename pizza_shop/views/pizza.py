from rest_framework import generics
from ..models import Pizza
from ..serializers import PizzaSerializer
from django.db.models import Q


class PizzaList(generics.ListAPIView):
    """
    List all pizzas(filter).
    """

    serializer_class = PizzaSerializer

    def get_queryset(self):
        token = self.request.query_params.get('token')
        availability = self.request.query_params.get('availability', None)
        min_price = self.request.query_params.get('min_price', 0)
        max_price = self.request.query_params.get('max_price', 10000)

        query_set = Pizza.objects.all()
        if token:
            query_set = query_set.filter(
                Q(name__icontains=token) |
                Q(brand__icontains=token) |
                Q(tags__icontains=token)
            )
        if availability is not None:
            query_set = query_set.filter(availability=availability)

        query_set = query_set.filter(price__gte=min_price, price__lte=max_price)

        return query_set


class PizzaDetail(generics.RetrieveAPIView):
    """
    Retrieve specified pizza details.
    """

    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer

from django.test import TestCase
from .models import CustomUser, Pizza
from rest_framework.test import APIClient
from rest_framework import status


# Test case for model
class PizzaModelTestCase(TestCase):
    """This class defines the test suite for the Pizza model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.pizza_name = "cheese"
        self.pizza_brand = "Brand"
        self.pizza_price = 300
        self.pizza_weight = 10
        self.pizza = Pizza(name=self.pizza_name, brand=self.pizza_brand, price=self.pizza_price, weight=self.pizza_weight)

    def test_model_can_create_a_pizza(self):
        """Test the Pizza model can create a pizza."""
        old_count = Pizza.objects.count()
        self.pizza.save()
        new_count = Pizza.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_get_a_pizza(self):
        self.pizza.save()
        pizza_from_db = Pizza.objects.get()
        self.assertEqual(pizza_from_db.name, self.pizza.name)

    def test_model_can_update_a_pizza(self):
        self.pizza.save()
        old_pizza = Pizza.objects.get()
        old_pizza.name = 'new_pizza'
        old_pizza.save()
        pizza_from_db = Pizza.objects.filter(name='new_pizza')[0]
        self.assertEqual('new_pizza', pizza_from_db.name)


class UserModelTestCase(TestCase):
    """This class defines the test suite for the User model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = CustomUser(email='sujon.sun@yahoo.com', phone='01762700200', password='abc123')

    def test_model_can_create_a_user(self):
        old_count = CustomUser.objects.count()
        self.user.save()
        new_count = CustomUser.objects.count()
        self.assertNotEqual(old_count, new_count)


# Test Case for views
class PizzaViewTestCase(TestCase):
    """Test suite for the pizza views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.pizza = {
            'name': 'cheese',
            'brand': 'regular',
            'price': 300,
            'weight': 10
        }
        self.response = self.client.post(
            '/shop/pizza/',
            self.pizza,
            format="json"
        )

    def test_api_can_create_a_pizza(self):
        """Test the api has pizza creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_pizza(self):
        """Test the api can get pizza."""
        response = self.client.get(
            '/shop/pizza/',
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewTestCase(TestCase):
    """Test suite for the user views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

    def test_api_will_give_401_for_unauthorized_user(self):
        """Test the api has user creation capability."""
        user = {
            'phone': '01762700280',
            'password': 'abc123'
        }
        response = self.client.post(
            '/user/login/',
            user,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



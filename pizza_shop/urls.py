from .views import PizzaShop, PizzaDetail, OrderList
from .user_views import Login, Profile
from django.urls import path

urlpatterns = [
    #user
    path('user/login/', Login.as_view()),
    path('user/profile/', Profile.as_view()),

    # pizza and order
    path('shop/pizza/', PizzaShop.as_view()),
    path('shop/pizza/<int:pk>/', PizzaDetail.as_view()),
    path('shop/order/', OrderList.as_view()),
]

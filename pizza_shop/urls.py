from .views import PizzaShop, PizzaDetail, OrderList, OrderDetail
from .user_views import Login, Profile
from django.urls import path

urlpatterns = [
    # user
    path('user/login/', Login.as_view()),
    path('user/profile/', Profile.as_view()),
    # pizza
    path('shop/pizza/', PizzaShop.as_view()),
    path('shop/pizza/<int:pk>/', PizzaDetail.as_view()),
    # order
    path('shop/order/', OrderList.as_view()),
    path('shop/order/<int:pk>', OrderDetail.as_view()),
]

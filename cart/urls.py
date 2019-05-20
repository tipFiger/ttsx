
from django.urls import path

from cart.views import *

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('add_cart/',add_cart, name='add_cart'),
    path('count_cart/',count_cart, name='count_cart'),
    path('change_cart/<int:id>/',change_cart, name='change_cart'),
    path('del_cart/<int:id>/',del_cart, name='del_cart'),

]
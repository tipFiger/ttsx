from django.urls import path

from order.views import *

urlpatterns = [
    path('place_order/', place_order, name='place_order'),
    path('make_order/', make_order, name='make_order'),
]

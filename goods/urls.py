
from django.urls import path

from goods.views import *
# detail,goodlist
urlpatterns = [
    path('index/', index, name='index'),
    path('logout/', logout, name='logout'),
    path('detail/<int:id>/', detail, name='detail'),
    path('goodlist/', goodlist, name='goodlist'),

]

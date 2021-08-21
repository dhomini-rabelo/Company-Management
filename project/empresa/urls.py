from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('minha-conta/', minha_conta, name='minha_conta'),
    path('minha-conta/editar/', editar_conta, name='editar_conta'),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('detalhar/<str:data>', detalhar, name='detalhar'),
    path('suspeitas/', suspeitas, name='suspeitas'),
]

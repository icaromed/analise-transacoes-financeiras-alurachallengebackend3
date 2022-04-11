from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('printar/', views.printar_console, name='printar')
]

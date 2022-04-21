from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<data>/detalhar', views.detalhar, name='detalhar')
]

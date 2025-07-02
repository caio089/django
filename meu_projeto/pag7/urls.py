from django.urls import path
from . import views

urlpatterns = [
    path('', views.pag7, name='pag7'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pag4, name='pag4'),
]
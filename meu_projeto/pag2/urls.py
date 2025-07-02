from django.urls import path
from . import views

urlpatterns = [
    path('', views.pag2, name='pag2'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.pag6, name='pag6'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pag5, name='pag5'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina7, name='pagina7'),
]
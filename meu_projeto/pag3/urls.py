from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina3, name='pagina3'),
]
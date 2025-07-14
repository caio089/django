from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina5, name='pagina5'),
]
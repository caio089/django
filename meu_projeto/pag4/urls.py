from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina4, name='pagina4'),
]
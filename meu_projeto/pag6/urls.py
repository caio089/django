from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina6, name='pagina6'),
]
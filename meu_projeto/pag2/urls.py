from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina2, name='pagina2'),
]

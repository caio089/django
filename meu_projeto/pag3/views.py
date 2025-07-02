from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def pagina1(request):
    return render(request, 'pagina3.html')

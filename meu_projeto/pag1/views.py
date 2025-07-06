from django.shortcuts import render

# Create your views here.

def pagina1(request):
    return render(request, 'pag1/pagina1.html')  # <-- repara nesse caminho


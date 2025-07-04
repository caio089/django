from django.shortcuts import render

# Create your views here.

def pagina1(request):
    return render(request, 'templates/pagina1.html')  # <-- repara nesse caminho


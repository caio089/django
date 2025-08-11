from django.shortcuts import render

# Create your views here.
def palavras(request):
    return render(request, 'palavras/palavras.html')
from django.shortcuts import render

# Create your views here.
def regras(request):
    return render(request, 'regras/regras.html')
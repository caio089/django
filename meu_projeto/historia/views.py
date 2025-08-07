from django.shortcuts import render

# Create your views here.
def historia(request):
    return render(request, 'historia/historia.html')  


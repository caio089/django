from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render

# Create your views here.

def index(request) :
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Substitua 'login' pelo nome da sua url de login
from django.shortcuts import render

# Create your views here.
def ukemis(request):
    return render(request, 'ukemi/ukemis.html', {'range10': range(1, 11)})
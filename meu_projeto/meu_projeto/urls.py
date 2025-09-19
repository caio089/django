"""
URL configuration for meu_projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('index/', include('core.urls')),
    path('pagina1/', include('pag1.urls')),
    path('pagina2/', include('pag2.urls')),
    path('pagina3/', include('pag3.urls')),
    path('pagina4/', include('pag4.urls')),
    path('pagina5/', include('pag5.urls')),
    path('pagina6/', include('pag6.urls')),
    path('pagina7/', include('pag7.urls')),
    path('ukemis/', include('ukemis.urls')),
    path('quiz/', include('quiz.urls')),
    path('historia/', include('historia.urls')),
    path('palavras/', include('palavras.urls')),  
    path('regras/', include('regras.urls')),
]

# Configuração para servir arquivos estáticos durante o desenvolvimento
# Esta configuração permite que o Django sirva arquivos estáticos (CSS, JS, imagens)
# diretamente durante o desenvolvimento local
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


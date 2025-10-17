from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import ProgressoElemento
import json

def pagina6(request):
    """View principal da página 6"""
    return render(request, 'pag6/pagina6.html')

@csrf_exempt
@require_http_methods(["POST"])
def salvar_progresso(request):
    """
    Salva o progresso dos elementos "Aprendi" no banco de dados
    """
    try:
        data = json.loads(request.body)
        pagina = data.get('pagina', 'pagina6')
        elementos = data.get('elementos', [])
        
        progressos_salvos = []
        
        for elemento in elementos:
            elemento_id = elemento.get('id')
            elemento_tipo = elemento.get('tipo')
            aprendido = elemento.get('aprendido', False)
            
            if not elemento_id or not elemento_tipo:
                continue
            
            # Usar sessão para usuários não logados
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            
            # Buscar ou criar progresso
            if request.user.is_authenticated:
                progresso, created = ProgressoElemento.objects.get_or_create(
                    usuario=request.user,
                    pagina=pagina,
                    elemento_id=elemento_id,
                    defaults={
                        'elemento_tipo': elemento_tipo,
                        'aprendido': aprendido,
                        'data_aprendizado': timezone.now() if aprendido else None
                    }
                )
            else:
                progresso, created = ProgressoElemento.objects.get_or_create(
                    session_key=session_key,
                    pagina=pagina,
                    elemento_id=elemento_id,
                    defaults={
                        'elemento_tipo': elemento_tipo,
                        'aprendido': aprendido,
                        'data_aprendizado': timezone.now() if aprendido else None
                    }
                )
            
            # Se já existe, atualizar
            if not created:
                progresso.aprendido = aprendido
                progresso.elemento_tipo = elemento_tipo
                if aprendido and not progresso.data_aprendizado:
                    progresso.data_aprendizado = timezone.now()
                elif not aprendido:
                    progresso.data_aprendizado = None
                progresso.save()
            
            progressos_salvos.append({
                'id': elemento_id,
                'tipo': elemento_tipo,
                'aprendido': progresso.aprendido,
                'data_aprendizado': progresso.data_aprendizado.isoformat() if progresso.data_aprendizado else None
            })
        
        return JsonResponse({
            'success': True,
            'message': f'Progresso salvo para {len(progressos_salvos)} elementos',
            'elementos': progressos_salvos
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def carregar_progresso(request):
    """
    Carrega o progresso dos elementos "Aprendi" do banco de dados
    """
    try:
        pagina = request.GET.get('pagina', 'pagina6')
        
        # Usar sessão para usuários não logados
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        if request.user.is_authenticated:
            progressos = ProgressoElemento.objects.filter(
                usuario=request.user,
                pagina=pagina
            )
        else:
            progressos = ProgressoElemento.objects.filter(
                session_key=session_key,
                pagina=pagina
            )
        
        elementos = []
        for progresso in progressos:
            elementos.append({
                'id': progresso.elemento_id,
                'tipo': progresso.elemento_tipo,
                'aprendido': progresso.aprendido,
                'data_aprendizado': progresso.data_aprendizado.isoformat() if progresso.data_aprendizado else None
            })
        
        return JsonResponse({
            'success': True,
            'elementos': elementos
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
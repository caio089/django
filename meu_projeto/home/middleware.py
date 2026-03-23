"""
Middleware para detectar faixa selecionada e redirecionar automaticamente
"""
import logging

logger = logging.getLogger(__name__)


class FaixaRedirectMiddleware:
    """
    Middleware que detecta a faixa selecionada pelo usuário e redireciona
    para a página correspondente automaticamente
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Processar a requisição antes da view
        response = self.process_request(request)
        
        if response:
            return response
        
        # Chamar a próxima view/middleware
        response = self.get_response(request)
        
        # Processar a resposta após a view
        return self.process_response(request, response)
    
    def process_request(self, request):
        """
        Processa a requisição antes da view ser chamada
        """
        # Só processar se o usuário estiver logado
        if not request.user.is_authenticated:
            return None
        
        # Verificar se há parâmetro de faixa na URL
        faixa = request.GET.get('faixa')
        if faixa:
            return self.redirect_to_faixa(faixa)
        
        # Verificar se há faixa salva na sessão
        faixa_sessao = request.session.get('faixa_selecionada')
        if faixa_sessao and request.path == '/':
            return self.redirect_to_faixa(faixa_sessao)
        
        return None
    
    def process_response(self, request, response):
        """
        Processa a resposta após a view ser chamada
        """
        return response
    
    def redirect_to_faixa(self, faixa):
        """
        Redireciona para a página da faixa correspondente
        """
        from django.http import HttpResponseRedirect
        
        # Mapeamento de faixas para URLs
        faixas_urls = {
            'branca': '/pagina1/',
            'amarela': '/pagina3/',
            'laranja': '/pagina4/',
            'verde': '/pagina5/',
            'azul': '/pagina2/',
            'marrom': '/pagina7/'
        }
        
        url_destino = faixas_urls.get(faixa.lower())
        if url_destino:
            return HttpResponseRedirect(url_destino)
        
        return None


class GoogleLoginMiddleware:
    """
    Middleware para processar dados do Google Login
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Processar dados do Google se presentes
        if request.method == 'POST' and 'google_data' in request.POST:
            self.process_google_data(request)
        
        response = self.get_response(request)
        return response
    
    def process_google_data(self, request):
        """
        Processa dados do Google Login
        """
        try:
            import json
            google_data = json.loads(request.POST.get('google_data'))
            
            # Salvar dados na sessão
            request.session['google_user'] = {
                'name': google_data.get('name'),
                'email': google_data.get('email'),
                'picture': google_data.get('picture')
            }
            
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar dados do Google: {e}")



"""
Comando para debug do sistema premium
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento
from home.models import Profile
from datetime import datetime

class Command(BaseCommand):
    help = 'Debug do sistema premium'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username do usuário')

    def handle(self, *args, **options):
        username = options.get('username')
        
        if username:
            try:
                user = User.objects.get(username=username)
                self.debug_user(user)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Usuário {username} não encontrado'))
        else:
            # Mostrar todos os usuários
            users = User.objects.all()
            self.stdout.write(f'Total de usuários: {users.count()}')
            for user in users:
                self.debug_user(user)
                self.stdout.write('-' * 50)

    def debug_user(self, user):
        self.stdout.write(f'\n🔍 DEBUG USUÁRIO: {user.username}')
        self.stdout.write(f'ID: {user.id}')
        self.stdout.write(f'Email: {user.email}')
        self.stdout.write(f'Ativo: {user.is_active}')
        self.stdout.write(f'Logado: {user.is_authenticated}')
        
        # Verificar Profile
        try:
            profile = user.profile
            self.stdout.write(f'Profile existe: Sim')
            self.stdout.write(f'Conta Premium: {profile.conta_premium}')
            self.stdout.write(f'Data Vencimento Premium: {profile.data_vencimento_premium}')
        except:
            self.stdout.write(f'Profile existe: NÃO')
        
        # Verificar Assinaturas
        assinaturas = Assinatura.objects.filter(usuario=user)
        self.stdout.write(f'Total de assinaturas: {assinaturas.count()}')
        
        for assinatura in assinaturas:
            self.stdout.write(f'  - ID: {assinatura.id}')
            self.stdout.write(f'  - Status: {assinatura.status}')
            self.stdout.write(f'  - Plano: {assinatura.plano.nome}')
            self.stdout.write(f'  - Data Início: {assinatura.data_inicio}')
            self.stdout.write(f'  - Data Vencimento: {assinatura.data_vencimento}')
            from django.utils import timezone
            self.stdout.write(f'  - Vencida: {assinatura.data_vencimento < timezone.now()}')
        
        # Verificar Pagamentos
        pagamentos = Pagamento.objects.filter(usuario=user)
        self.stdout.write(f'Total de pagamentos: {pagamentos.count()}')
        
        for pagamento in pagamentos:
            self.stdout.write(f'  - ID: {pagamento.id}')
            self.stdout.write(f'  - Status: {pagamento.status}')
            self.stdout.write(f'  - Valor: R$ {pagamento.valor}')
            self.stdout.write(f'  - Data: {pagamento.data_criacao}')
        
        # Testar verificação de acesso
        from payments.views import verificar_acesso_premium
        tem_acesso, assinatura = verificar_acesso_premium(user)
        self.stdout.write(f'✅ Tem acesso premium: {tem_acesso}')
        if assinatura:
            self.stdout.write(f'✅ Assinatura ativa: {assinatura.id}')

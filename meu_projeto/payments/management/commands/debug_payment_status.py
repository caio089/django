"""
Comando para debug do status de pagamento
Verifica se os dados estão sendo persistidos corretamente
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento, PlanoPremium
from home.models import Profile
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Debug do status de pagamento e assinaturas'

    def add_arguments(self, parser):
        parser.add_argument('--user-id', type=int, help='ID do usuário para verificar')
        parser.add_argument('--all', action='store_true', help='Verificar todos os usuários')

    def handle(self, *args, **options):
        self.stdout.write('🔍 Iniciando debug do status de pagamento...\n')
        
        if options['all']:
            self.debug_all_users()
        elif options['user_id']:
            self.debug_user(options['user_id'])
        else:
            self.stdout.write('Use --all para verificar todos ou --user-id ID para um usuário específico')

    def debug_all_users(self):
        """Debug de todos os usuários"""
        self.stdout.write('📊 Verificando todos os usuários...\n')
        
        # Contar usuários
        total_users = User.objects.count()
        self.stdout.write(f'Total de usuários: {total_users}')
        
        # Contar assinaturas
        total_assinaturas = Assinatura.objects.count()
        self.stdout.write(f'Total de assinaturas: {total_assinaturas}')
        
        # Contar pagamentos
        total_pagamentos = Pagamento.objects.count()
        self.stdout.write(f'Total de pagamentos: {total_pagamentos}')
        
        # Assinaturas ativas
        assinaturas_ativas = Assinatura.objects.filter(
            status='ativa',
            data_vencimento__gt=timezone.now()
        ).count()
        self.stdout.write(f'Assinaturas ativas: {assinaturas_ativas}')
        
        # Usuários com conta premium
        usuarios_premium = Profile.objects.filter(conta_premium=True).count()
        self.stdout.write(f'Usuários com conta premium: {usuarios_premium}')
        
        self.stdout.write('\n📋 Detalhes das assinaturas ativas:')
        assinaturas = Assinatura.objects.filter(
            status='ativa',
            data_vencimento__gt=timezone.now()
        ).select_related('usuario', 'plano')
        
        for assinatura in assinaturas:
            self.stdout.write(f'  - {assinatura.usuario.username} ({assinatura.usuario.profile.nome})')
            self.stdout.write(f'    Plano: {assinatura.plano.nome}')
            self.stdout.write(f'    Status: {assinatura.status}')
            self.stdout.write(f'    Vencimento: {assinatura.data_vencimento}')
            self.stdout.write(f'    Profile Premium: {assinatura.usuario.profile.conta_premium}')
            self.stdout.write('')

    def debug_user(self, user_id):
        """Debug de um usuário específico"""
        try:
            user = User.objects.get(id=user_id)
            self.stdout.write(f'👤 Debug do usuário: {user.username} ({user.profile.nome})\n')
            
            # Verificar perfil
            profile = user.profile
            self.stdout.write(f'📋 Perfil:')
            self.stdout.write(f'  - Nome: {profile.nome}')
            self.stdout.write(f'  - Conta Premium: {profile.conta_premium}')
            self.stdout.write(f'  - Data Vencimento Premium: {profile.data_vencimento_premium}')
            
            # Verificar assinaturas
            assinaturas = Assinatura.objects.filter(usuario=user)
            self.stdout.write(f'\n📋 Assinaturas ({assinaturas.count()}):')
            for assinatura in assinaturas:
                self.stdout.write(f'  - ID: {assinatura.id}')
                self.stdout.write(f'    Plano: {assinatura.plano.nome}')
                self.stdout.write(f'    Status: {assinatura.status}')
                self.stdout.write(f'    Início: {assinatura.data_inicio}')
                self.stdout.write(f'    Vencimento: {assinatura.data_vencimento}')
                self.stdout.write(f'    Ativa: {assinatura.ativo}')
                self.stdout.write(f'    External Reference: {assinatura.external_reference}')
            
            # Verificar pagamentos
            pagamentos = Pagamento.objects.filter(usuario=user)
            self.stdout.write(f'\n💳 Pagamentos ({pagamentos.count()}):')
            for pagamento in pagamentos:
                self.stdout.write(f'  - ID: {pagamento.id}')
                self.stdout.write(f'    Valor: R$ {pagamento.valor}')
                self.stdout.write(f'    Status: {pagamento.status}')
                self.stdout.write(f'    Data: {pagamento.data_pagamento}')
                self.stdout.write(f'    Payment ID: {pagamento.get_payment_id()}')
                self.stdout.write(f'    External Reference: {pagamento.external_reference}')
            
            # Verificar acesso premium
            from payments.views import verificar_acesso_premium
            tem_acesso, assinatura = verificar_acesso_premium(user)
            self.stdout.write(f'\n🔐 Verificação de acesso premium:')
            self.stdout.write(f'  - Tem acesso: {tem_acesso}')
            self.stdout.write(f'  - Assinatura: {assinatura.id if assinatura else "Nenhuma"}')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuário com ID {user_id} não encontrado'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao verificar usuário: {e}'))

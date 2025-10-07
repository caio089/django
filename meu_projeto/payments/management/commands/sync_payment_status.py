"""
Comando para sincronizar status de pagamento
Força a atualização do status premium baseado nas assinaturas ativas
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento
from home.models import Profile
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sincroniza status de pagamento baseado nas assinaturas ativas'

    def add_arguments(self, parser):
        parser.add_argument('--user-id', type=int, help='ID do usuário para sincronizar')
        parser.add_argument('--all', action='store_true', help='Sincronizar todos os usuários')
        parser.add_argument('--force', action='store_true', help='Forçar sincronização mesmo se já estiver correto')

    def handle(self, *args, **options):
        self.stdout.write('🔄 Iniciando sincronização do status de pagamento...\n')
        
        if options['all']:
            self.sync_all_users(options['force'])
        elif options['user_id']:
            self.sync_user(options['user_id'], options['force'])
        else:
            self.stdout.write('Use --all para sincronizar todos ou --user-id ID para um usuário específico')

    def sync_all_users(self, force=False):
        """Sincroniza todos os usuários"""
        self.stdout.write('📊 Sincronizando todos os usuários...\n')
        
        usuarios_atualizados = 0
        usuarios_verificados = 0
        
        for user in User.objects.all():
            if self.sync_user_profile(user, force):
                usuarios_atualizados += 1
            usuarios_verificados += 1
        
        self.stdout.write(f'\n✅ Sincronização concluída:')
        self.stdout.write(f'  - Usuários verificados: {usuarios_verificados}')
        self.stdout.write(f'  - Usuários atualizados: {usuarios_atualizados}')

    def sync_user(self, user_id, force=False):
        """Sincroniza um usuário específico"""
        try:
            user = User.objects.get(id=user_id)
            self.stdout.write(f'👤 Sincronizando usuário: {user.username} ({user.profile.nome})\n')
            
            if self.sync_user_profile(user, force):
                self.stdout.write('✅ Usuário sincronizado com sucesso!')
            else:
                self.stdout.write('ℹ️ Usuário já estava sincronizado')
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuário com ID {user_id} não encontrado'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao sincronizar usuário: {e}'))

    def sync_user_profile(self, user, force=False):
        """Sincroniza o perfil de um usuário baseado nas assinaturas"""
        try:
            profile = user.profile
            
            # Verificar se tem assinatura ativa
            assinatura_ativa = Assinatura.objects.filter(
                usuario=user,
                status='ativa',
                data_vencimento__gt=timezone.now()
            ).first()
            
            # Determinar se deve ter acesso premium
            deve_ter_premium = assinatura_ativa is not None
            
            # Verificar se precisa atualizar
            precisa_atualizar = (
                profile.conta_premium != deve_ter_premium or
                (deve_ter_premium and assinatura_ativa and 
                 profile.data_vencimento_premium != assinatura_ativa.data_vencimento)
            )
            
            if not precisa_atualizar and not force:
                return False
            
            # Atualizar perfil
            profile.conta_premium = deve_ter_premium
            if assinatura_ativa:
                profile.data_vencimento_premium = assinatura_ativa.data_vencimento
            else:
                profile.data_vencimento_premium = None
            
            profile.save()
            
            self.stdout.write(f'  📝 Perfil atualizado:')
            self.stdout.write(f'    - Conta Premium: {profile.conta_premium}')
            self.stdout.write(f'    - Data Vencimento: {profile.data_vencimento_premium}')
            
            if assinatura_ativa:
                self.stdout.write(f'    - Assinatura: {assinatura_ativa.plano.nome}')
                self.stdout.write(f'    - Status: {assinatura_ativa.status}')
            
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao sincronizar perfil do usuário {user.username}: {e}'))
            return False

    def check_inconsistencies(self):
        """Verifica inconsistências entre assinaturas e perfis"""
        self.stdout.write('🔍 Verificando inconsistências...\n')
        
        inconsistencias = []
        
        for user in User.objects.all():
            profile = user.profile
            
            # Verificar se tem assinatura ativa
            assinatura_ativa = Assinatura.objects.filter(
                usuario=user,
                status='ativa',
                data_vencimento__gt=timezone.now()
            ).first()
            
            # Verificar inconsistências
            if assinatura_ativa and not profile.conta_premium:
                inconsistencias.append({
                    'user': user.username,
                    'tipo': 'Assinatura ativa mas perfil não premium',
                    'assinatura': assinatura_ativa.id,
                    'profile_premium': profile.conta_premium
                })
            
            elif not assinatura_ativa and profile.conta_premium:
                inconsistencias.append({
                    'user': user.username,
                    'tipo': 'Perfil premium mas sem assinatura ativa',
                    'assinatura': 'Nenhuma',
                    'profile_premium': profile.conta_premium
                })
        
        if inconsistencias:
            self.stdout.write(f'⚠️ Encontradas {len(inconsistencias)} inconsistências:')
            for inc in inconsistencias:
                self.stdout.write(f'  - {inc["user"]}: {inc["tipo"]}')
        else:
            self.stdout.write('✅ Nenhuma inconsistência encontrada!')
        
        return inconsistencias

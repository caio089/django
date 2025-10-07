"""
Comando para executar após cada deploy
Sincroniza todos os dados de pagamento e garante consistência
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento
from home.models import Profile
from django.utils import timezone
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sincronização pós-deploy para garantir persistência de dados'

    def add_arguments(self, parser):
        parser.add_argument('--verbose', action='store_true', help='Mostrar detalhes da sincronização')
        parser.add_argument('--force', action='store_true', help='Forçar sincronização mesmo se não houver problemas')

    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando sincronização pós-deploy...\n')
        
        verbose = options['verbose']
        force = options['force']
        
        with transaction.atomic():
            # 1. Verificar e corrigir perfis ausentes
            self.fix_missing_profiles(verbose)
            
            # 2. Sincronizar status premium
            self.sync_premium_status(verbose, force)
            
            # 3. Corrigir assinaturas expiradas
            self.fix_expired_subscriptions(verbose)
            
            # 4. Verificar integridade dos dados
            self.check_data_integrity(verbose)
        
        self.stdout.write('\n✅ Sincronização pós-deploy concluída!')

    def fix_missing_profiles(self, verbose):
        """Corrige perfis ausentes"""
        if verbose:
            self.stdout.write('🔧 Verificando perfis ausentes...')
        
        usuarios_sem_perfil = User.objects.filter(profile__isnull=True)
        count = 0
        
        for user in usuarios_sem_perfil:
            Profile.objects.create(
                user=user,
                nome=user.username,
                idade=18,
                faixa='branca'
            )
            count += 1
            if verbose:
                self.stdout.write(f'  ✅ Perfil criado para: {user.username}')
        
        if count > 0:
            self.stdout.write(f'📊 Perfis criados: {count}')
        elif verbose:
            self.stdout.write('  ℹ️ Nenhum perfil ausente encontrado')

    def sync_premium_status(self, verbose, force):
        """Sincroniza status premium de todos os usuários"""
        if verbose:
            self.stdout.write('🔄 Sincronizando status premium...')
        
        usuarios_atualizados = 0
        
        for user in User.objects.all():
            try:
                profile = user.profile
                
                # Verificar se tem assinatura ativa
                assinatura_ativa = Assinatura.objects.filter(
                    usuario=user,
                    status='ativa',
                    data_vencimento__gt=timezone.now()
                ).first()
                
                # Determinar status correto
                deve_ter_premium = assinatura_ativa is not None
                
                # Verificar se precisa atualizar
                precisa_atualizar = (
                    profile.conta_premium != deve_ter_premium or
                    (deve_ter_premium and assinatura_ativa and 
                     profile.data_vencimento_premium != assinatura_ativa.data_vencimento)
                )
                
                if precisa_atualizar or force:
                    # Atualizar perfil
                    profile.conta_premium = deve_ter_premium
                    if assinatura_ativa:
                        profile.data_vencimento_premium = assinatura_ativa.data_vencimento
                    else:
                        profile.data_vencimento_premium = None
                    
                    profile.save()
                    usuarios_atualizados += 1
                    
                    if verbose:
                        status = "Premium" if deve_ter_premium else "Básico"
                        self.stdout.write(f'  ✅ {user.username}: {status}')
            
            except Exception as e:
                if verbose:
                    self.stdout.write(f'  ❌ Erro em {user.username}: {e}')
                logger.error(f"Erro ao sincronizar {user.username}: {e}")
        
        self.stdout.write(f'📊 Usuários atualizados: {usuarios_atualizados}')

    def fix_expired_subscriptions(self, verbose):
        """Corrige assinaturas expiradas"""
        if verbose:
            self.stdout.write('⏰ Verificando assinaturas expiradas...')
        
        assinaturas_expiradas = Assinatura.objects.filter(
            status='ativa',
            data_vencimento__lt=timezone.now()
        )
        
        count = 0
        for assinatura in assinaturas_expiradas:
            assinatura.status = 'expirada'
            assinatura.save()
            count += 1
            
            if verbose:
                self.stdout.write(f'  ✅ Assinatura expirada: {assinatura.usuario.username}')
        
        if count > 0:
            self.stdout.write(f'📊 Assinaturas expiradas corrigidas: {count}')
        elif verbose:
            self.stdout.write('  ℹ️ Nenhuma assinatura expirada encontrada')

    def check_data_integrity(self, verbose):
        """Verifica integridade dos dados"""
        if verbose:
            self.stdout.write('🔍 Verificando integridade dos dados...')
        
        problemas = []
        
        # Verificar usuários sem perfil
        usuarios_sem_perfil = User.objects.filter(profile__isnull=True).count()
        if usuarios_sem_perfil > 0:
            problemas.append(f'Usuários sem perfil: {usuarios_sem_perfil}')
        
        # Verificar assinaturas órfãs
        assinaturas_orfa = Assinatura.objects.filter(usuario__isnull=True).count()
        if assinaturas_orfa > 0:
            problemas.append(f'Assinaturas órfãs: {assinaturas_orfa}')
        
        # Verificar pagamentos órfãos
        pagamentos_orfa = Pagamento.objects.filter(usuario__isnull=True).count()
        if pagamentos_orfa > 0:
            problemas.append(f'Pagamentos órfãos: {pagamentos_orfa}')
        
        # Verificar inconsistências de status premium
        inconsistencias = 0
        for user in User.objects.all():
            try:
                profile = user.profile
                assinatura_ativa = Assinatura.objects.filter(
                    usuario=user,
                    status='ativa',
                    data_vencimento__gt=timezone.now()
                ).exists()
                
                if profile.conta_premium != assinatura_ativa:
                    inconsistencias += 1
            except:
                inconsistencias += 1
        
        if inconsistencias > 0:
            problemas.append(f'Inconsistências de status premium: {inconsistencias}')
        
        if problemas:
            self.stdout.write('⚠️ Problemas encontrados:')
            for problema in problemas:
                self.stdout.write(f'  - {problema}')
        elif verbose:
            self.stdout.write('  ✅ Nenhum problema de integridade encontrado')
        
        # Estatísticas finais
        total_usuarios = User.objects.count()
        total_assinaturas = Assinatura.objects.count()
        total_pagamentos = Pagamento.objects.count()
        assinaturas_ativas = Assinatura.objects.filter(
            status='ativa',
            data_vencimento__gt=timezone.now()
        ).count()
        usuarios_premium = Profile.objects.filter(conta_premium=True).count()
        
        self.stdout.write(f'\n📊 Estatísticas finais:')
        self.stdout.write(f'  - Total de usuários: {total_usuarios}')
        self.stdout.write(f'  - Total de assinaturas: {total_assinaturas}')
        self.stdout.write(f'  - Assinaturas ativas: {assinaturas_ativas}')
        self.stdout.write(f'  - Total de pagamentos: {total_pagamentos}')
        self.stdout.write(f'  - Usuários premium: {usuarios_premium}')
        
        if len(problemas) == 0:
            self.stdout.write('✅ Todos os dados estão íntegros!')

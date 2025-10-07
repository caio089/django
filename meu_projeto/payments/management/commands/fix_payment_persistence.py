"""
Comando para corrigir problemas de persistência de pagamento
Garante que os dados sejam mantidos após deploy
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento, PlanoPremium
from home.models import Profile
from django.utils import timezone
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Corrige problemas de persistência de pagamento'

    def add_arguments(self, parser):
        parser.add_argument('--check', action='store_true', help='Apenas verificar problemas')
        parser.add_argument('--fix', action='store_true', help='Corrigir problemas encontrados')
        parser.add_argument('--backup', action='store_true', help='Criar backup dos dados')

    def handle(self, *args, **options):
        self.stdout.write('🔧 Iniciando verificação de persistência de pagamento...\n')
        
        if options['backup']:
            self.create_backup()
        
        if options['check']:
            self.check_persistence()
        elif options['fix']:
            self.fix_persistence()
        else:
            self.stdout.write('Use --check para verificar ou --fix para corrigir')

    def create_backup(self):
        """Cria backup dos dados importantes"""
        self.stdout.write('💾 Criando backup dos dados...\n')
        
        backup_data = {
            'usuarios': [],
            'assinaturas': [],
            'pagamentos': [],
            'perfis': []
        }
        
        # Backup de usuários
        for user in User.objects.all():
            backup_data['usuarios'].append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'date_joined': user.date_joined.isoformat()
            })
        
        # Backup de assinaturas
        for assinatura in Assinatura.objects.all():
            backup_data['assinaturas'].append({
                'id': assinatura.id,
                'usuario_id': assinatura.usuario.id,
                'plano_id': assinatura.plano.id,
                'status': assinatura.status,
                'data_inicio': assinatura.data_inicio.isoformat(),
                'data_vencimento': assinatura.data_vencimento.isoformat(),
                'external_reference': str(assinatura.external_reference),
                'subscription_id': assinatura.subscription_id
            })
        
        # Backup de pagamentos
        for pagamento in Pagamento.objects.all():
            backup_data['pagamentos'].append({
                'id': pagamento.id,
                'usuario_id': pagamento.usuario.id,
                'valor': float(pagamento.valor),
                'status': pagamento.status,
                'payment_id': pagamento.get_payment_id(),
                'external_reference': str(pagamento.external_reference),
                'data_pagamento': pagamento.data_pagamento.isoformat() if pagamento.data_pagamento else None
            })
        
        # Backup de perfis
        for profile in Profile.objects.all():
            backup_data['perfis'].append({
                'user_id': profile.user.id,
                'nome': profile.nome,
                'conta_premium': profile.conta_premium,
                'data_vencimento_premium': profile.data_vencimento_premium.isoformat() if profile.data_vencimento_premium else None
            })
        
        # Salvar backup em arquivo
        import json
        from datetime import datetime
        
        backup_filename = f'backup_payment_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(f'✅ Backup criado: {backup_filename}')
        self.stdout.write(f'  - Usuários: {len(backup_data["usuarios"])}')
        self.stdout.write(f'  - Assinaturas: {len(backup_data["assinaturas"])}')
        self.stdout.write(f'  - Pagamentos: {len(backup_data["pagamentos"])}')
        self.stdout.write(f'  - Perfis: {len(backup_data["perfis"])}')

    def check_persistence(self):
        """Verifica problemas de persistência"""
        self.stdout.write('🔍 Verificando problemas de persistência...\n')
        
        problemas = []
        
        # Verificar usuários sem perfil
        usuarios_sem_perfil = User.objects.filter(profile__isnull=True)
        if usuarios_sem_perfil.exists():
            problemas.append({
                'tipo': 'Usuários sem perfil',
                'quantidade': usuarios_sem_perfil.count(),
                'detalhes': [u.username for u in usuarios_sem_perfil]
            })
        
        # Verificar assinaturas órfãs (sem usuário)
        assinaturas_orfa = Assinatura.objects.filter(usuario__isnull=True)
        if assinaturas_orfa.exists():
            problemas.append({
                'tipo': 'Assinaturas órfãs',
                'quantidade': assinaturas_orfa.count(),
                'detalhes': [str(a.id) for a in assinaturas_orfa]
            })
        
        # Verificar pagamentos órfãos
        pagamentos_orfa = Pagamento.objects.filter(usuario__isnull=True)
        if pagamentos_orfa.exists():
            problemas.append({
                'tipo': 'Pagamentos órfãos',
                'quantidade': pagamentos_orfa.count(),
                'detalhes': [str(p.id) for p in pagamentos_orfa]
            })
        
        # Verificar inconsistências de status premium
        inconsistencias = self.check_premium_inconsistencies()
        if inconsistencias:
            problemas.append({
                'tipo': 'Inconsistências de status premium',
                'quantidade': len(inconsistencias),
                'detalhes': inconsistencias
            })
        
        # Verificar assinaturas expiradas não atualizadas
        assinaturas_expiradas = Assinatura.objects.filter(
            status='ativa',
            data_vencimento__lt=timezone.now()
        )
        if assinaturas_expiradas.exists():
            problemas.append({
                'tipo': 'Assinaturas expiradas não atualizadas',
                'quantidade': assinaturas_expiradas.count(),
                'detalhes': [f'{a.usuario.username} - {a.data_vencimento}' for a in assinaturas_expiradas]
            })
        
        if problemas:
            self.stdout.write('⚠️ Problemas encontrados:')
            for problema in problemas:
                self.stdout.write(f'  - {problema["tipo"]}: {problema["quantidade"]} itens')
                for detalhe in problema["detalhes"][:5]:  # Mostrar apenas os primeiros 5
                    self.stdout.write(f'    * {detalhe}')
                if len(problema["detalhes"]) > 5:
                    self.stdout.write(f'    ... e mais {len(problema["detalhes"]) - 5} itens')
        else:
            self.stdout.write('✅ Nenhum problema encontrado!')

    def fix_persistence(self):
        """Corrige problemas de persistência"""
        self.stdout.write('🔧 Corrigindo problemas de persistência...\n')
        
        with transaction.atomic():
            # Corrigir usuários sem perfil
            usuarios_sem_perfil = User.objects.filter(profile__isnull=True)
            for user in usuarios_sem_perfil:
                Profile.objects.create(
                    user=user,
                    nome=user.username,
                    idade=18,
                    faixa='branca'
                )
                self.stdout.write(f'✅ Perfil criado para usuário: {user.username}')
            
            # Corrigir assinaturas expiradas
            assinaturas_expiradas = Assinatura.objects.filter(
                status='ativa',
                data_vencimento__lt=timezone.now()
            )
            for assinatura in assinaturas_expiradas:
                assinatura.status = 'expirada'
                assinatura.save()
                
                # Atualizar perfil do usuário
                try:
                    profile = assinatura.usuario.profile
                    profile.conta_premium = False
                    profile.data_vencimento_premium = None
                    profile.save()
                    self.stdout.write(f'✅ Assinatura expirada atualizada: {assinatura.usuario.username}')
                except:
                    self.stdout.write(f'⚠️ Erro ao atualizar perfil: {assinatura.usuario.username}')
            
            # Sincronizar status premium
            self.sync_all_premium_status()
        
        self.stdout.write('✅ Correções aplicadas com sucesso!')

    def check_premium_inconsistencies(self):
        """Verifica inconsistências de status premium"""
        inconsistencias = []
        
        for user in User.objects.all():
            try:
                profile = user.profile
                
                # Verificar se tem assinatura ativa
                assinatura_ativa = Assinatura.objects.filter(
                    usuario=user,
                    status='ativa',
                    data_vencimento__gt=timezone.now()
                ).first()
                
                # Verificar inconsistências
                if assinatura_ativa and not profile.conta_premium:
                    inconsistencias.append(f'{user.username}: Assinatura ativa mas perfil não premium')
                elif not assinatura_ativa and profile.conta_premium:
                    inconsistencias.append(f'{user.username}: Perfil premium mas sem assinatura ativa')
                    
            except Exception as e:
                inconsistencias.append(f'{user.username}: Erro ao verificar - {e}')
        
        return inconsistencias

    def sync_all_premium_status(self):
        """Sincroniza status premium de todos os usuários"""
        self.stdout.write('🔄 Sincronizando status premium...')
        
        for user in User.objects.all():
            try:
                profile = user.profile
                
                # Verificar se tem assinatura ativa
                assinatura_ativa = Assinatura.objects.filter(
                    usuario=user,
                    status='ativa',
                    data_vencimento__gt=timezone.now()
                ).first()
                
                # Atualizar perfil
                profile.conta_premium = assinatura_ativa is not None
                if assinatura_ativa:
                    profile.data_vencimento_premium = assinatura_ativa.data_vencimento
                else:
                    profile.data_vencimento_premium = None
                
                profile.save()
                
            except Exception as e:
                self.stdout.write(f'⚠️ Erro ao sincronizar {user.username}: {e}')
        
        self.stdout.write('✅ Status premium sincronizado!')

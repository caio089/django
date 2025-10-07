"""
Sistema de sincronização automática na inicialização do Django
Executa automaticamente após cada deploy/restart
"""
import logging
from django.db import transaction
from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento
from home.models import Profile
from django.utils import timezone
import threading
import time

logger = logging.getLogger(__name__)

class StartupPaymentSync:
    """
    Classe para sincronização automática de pagamentos na inicialização
    """
    
    _sync_executed = False
    _sync_lock = threading.Lock()
    
    @classmethod
    def run_automatic_sync(cls):
        """
        Executa sincronização automática de forma thread-safe
        """
        with cls._sync_lock:
            if cls._sync_executed:
                return
            
            # Executar em thread separada para não bloquear a inicialização
            thread = threading.Thread(target=cls._perform_sync, daemon=True)
            thread.start()
            cls._sync_executed = True
    
    @classmethod
    def _perform_sync(cls):
        """
        Executa a sincronização em background
        """
        try:
            # Aguardar um pouco para garantir que o Django esteja totalmente carregado
            time.sleep(2)
            
            logger.info("🚀 Iniciando sincronização automática de pagamentos...")
            
            with transaction.atomic():
                # 1. Corrigir perfis ausentes
                cls._fix_missing_profiles()
                
                # 2. Sincronizar status premium
                cls._sync_premium_status()
                
                # 3. Corrigir assinaturas expiradas
                cls._fix_expired_subscriptions()
                
                # 4. Verificar integridade
                cls._check_data_integrity()
            
            logger.info("✅ Sincronização automática concluída com sucesso!")
            
        except Exception as e:
            logger.error(f"❌ Erro na sincronização automática: {e}")
    
    @classmethod
    def _fix_missing_profiles(cls):
        """Corrige perfis ausentes"""
        try:
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
            
            if count > 0:
                logger.info(f"📊 Perfis criados automaticamente: {count}")
                
        except Exception as e:
            logger.error(f"Erro ao corrigir perfis ausentes: {e}")
    
    @classmethod
    def _sync_premium_status(cls):
        """Sincroniza status premium de todos os usuários"""
        try:
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
                    
                    if precisa_atualizar:
                        # Atualizar perfil
                        profile.conta_premium = deve_ter_premium
                        if assinatura_ativa:
                            profile.data_vencimento_premium = assinatura_ativa.data_vencimento
                        else:
                            profile.data_vencimento_premium = None
                        
                        profile.save()
                        usuarios_atualizados += 1
                        
                        logger.info(f"🔄 Status sincronizado: {user.username} -> {'Premium' if deve_ter_premium else 'Básico'}")
                
                except Exception as e:
                    logger.error(f"Erro ao sincronizar {user.username}: {e}")
            
            if usuarios_atualizados > 0:
                logger.info(f"📊 Usuários sincronizados: {usuarios_atualizados}")
                
        except Exception as e:
            logger.error(f"Erro na sincronização de status premium: {e}")
    
    @classmethod
    def _fix_expired_subscriptions(cls):
        """Corrige assinaturas expiradas"""
        try:
            assinaturas_expiradas = Assinatura.objects.filter(
                status='ativa',
                data_vencimento__lt=timezone.now()
            )
            
            count = 0
            for assinatura in assinaturas_expiradas:
                assinatura.status = 'expirada'
                assinatura.save()
                count += 1
                
                # Atualizar perfil do usuário
                try:
                    profile = assinatura.usuario.profile
                    profile.conta_premium = False
                    profile.data_vencimento_premium = None
                    profile.save()
                    logger.info(f"⏰ Assinatura expirada: {assinatura.usuario.username}")
                except:
                    pass
            
            if count > 0:
                logger.info(f"📊 Assinaturas expiradas corrigidas: {count}")
                
        except Exception as e:
            logger.error(f"Erro ao corrigir assinaturas expiradas: {e}")
    
    @classmethod
    def _check_data_integrity(cls):
        """Verifica integridade dos dados"""
        try:
            # Estatísticas
            total_usuarios = User.objects.count()
            total_assinaturas = Assinatura.objects.count()
            total_pagamentos = Pagamento.objects.count()
            assinaturas_ativas = Assinatura.objects.filter(
                status='ativa',
                data_vencimento__gt=timezone.now()
            ).count()
            usuarios_premium = Profile.objects.filter(conta_premium=True).count()
            
            logger.info(f"📊 Estatísticas finais:")
            logger.info(f"  - Usuários: {total_usuarios}")
            logger.info(f"  - Assinaturas: {total_assinaturas}")
            logger.info(f"  - Assinaturas ativas: {assinaturas_ativas}")
            logger.info(f"  - Pagamentos: {total_pagamentos}")
            logger.info(f"  - Usuários premium: {usuarios_premium}")
            
        except Exception as e:
            logger.error(f"Erro na verificação de integridade: {e}")

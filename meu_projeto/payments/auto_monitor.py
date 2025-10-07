"""
Sistema de monitoramento automático de pagamentos
Verifica e corrige problemas automaticamente
"""
import logging
import threading
import time
from django.db import transaction
from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento
from home.models import Profile
from django.utils import timezone

logger = logging.getLogger(__name__)

class AutoMonitor:
    """
    Monitor automático que verifica e corrige problemas
    """
    
    _monitoring = False
    _monitor_thread = None
    
    @classmethod
    def start_monitoring(cls):
        """
        Inicia monitoramento automático
        """
        if cls._monitoring:
            return
        
        cls._monitoring = True
        cls._monitor_thread = threading.Thread(target=cls._monitor_loop, daemon=True)
        cls._monitor_thread.start()
        logger.info("🔍 Monitor automático iniciado")
    
    @classmethod
    def stop_monitoring(cls):
        """
        Para o monitoramento automático
        """
        cls._monitoring = False
        if cls._monitor_thread:
            cls._monitor_thread.join(timeout=5)
        logger.info("🔍 Monitor automático parado")
    
    @classmethod
    def _monitor_loop(cls):
        """
        Loop principal do monitoramento
        """
        while cls._monitoring:
            try:
                # Aguardar 30 minutos
                time.sleep(1800)
                
                if cls._monitoring:
                    cls._perform_health_check()
                    
            except Exception as e:
                logger.error(f"Erro no monitor automático: {e}")
    
    @classmethod
    def _perform_health_check(cls):
        """
        Executa verificação de saúde do sistema
        """
        try:
            logger.info("🔍 Executando verificação de saúde automática...")
            
            with transaction.atomic():
                # 1. Verificar e corrigir perfis ausentes
                cls._check_missing_profiles()
                
                # 2. Verificar e corrigir inconsistências de status
                cls._check_premium_inconsistencies()
                
                # 3. Verificar e corrigir assinaturas expiradas
                cls._check_expired_subscriptions()
                
                # 4. Verificar integridade dos dados
                cls._check_data_integrity()
            
            logger.info("✅ Verificação de saúde concluída")
            
            # Enviar notificação se necessário
            try:
                from .auto_notifications import AutoNotificationManager
                AutoNotificationManager.send_system_health_report()
            except Exception as e:
                logger.error(f"Erro ao enviar notificação: {e}")
            
        except Exception as e:
            logger.error(f"Erro na verificação de saúde: {e}")
    
    @classmethod
    def _check_missing_profiles(cls):
        """Verifica e corrige perfis ausentes"""
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
                logger.info(f"🔧 Perfil criado automaticamente: {user.username}")
            
            if count > 0:
                logger.info(f"📊 Perfis criados: {count}")
                
        except Exception as e:
            logger.error(f"Erro ao verificar perfis ausentes: {e}")
    
    @classmethod
    def _check_premium_inconsistencies(cls):
        """Verifica e corrige inconsistências de status premium"""
        try:
            inconsistencias = 0
            
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
                    if profile.conta_premium != (assinatura_ativa is not None):
                        # Corrigir inconsistência
                        profile.conta_premium = assinatura_ativa is not None
                        if assinatura_ativa:
                            profile.data_vencimento_premium = assinatura_ativa.data_vencimento
                        else:
                            profile.data_vencimento_premium = None
                        
                        profile.save()
                        inconsistencias += 1
                        logger.info(f"🔧 Inconsistência corrigida: {user.username}")
                
                except Exception as e:
                    logger.error(f"Erro ao verificar {user.username}: {e}")
            
            if inconsistencias > 0:
                logger.info(f"📊 Inconsistências corrigidas: {inconsistencias}")
                
        except Exception as e:
            logger.error(f"Erro ao verificar inconsistências: {e}")
    
    @classmethod
    def _check_expired_subscriptions(cls):
        """Verifica e corrige assinaturas expiradas"""
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
            logger.error(f"Erro ao verificar assinaturas expiradas: {e}")
    
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
            
            # Verificar proporções
            if total_usuarios > 0:
                premium_ratio = usuarios_premium / total_usuarios
                if premium_ratio > 0.5:  # Mais de 50% premium pode indicar problema
                    logger.warning(f"⚠️ Alto percentual de usuários premium: {premium_ratio:.2%}")
            
            logger.info(f"📊 Status do sistema:")
            logger.info(f"  - Usuários: {total_usuarios}")
            logger.info(f"  - Assinaturas: {total_assinaturas}")
            logger.info(f"  - Assinaturas ativas: {assinaturas_ativas}")
            logger.info(f"  - Pagamentos: {total_pagamentos}")
            logger.info(f"  - Usuários premium: {usuarios_premium}")
            
        except Exception as e:
            logger.error(f"Erro na verificação de integridade: {e}")
    
    @classmethod
    def force_sync_all(cls):
        """
        Força sincronização completa de todos os usuários
        """
        try:
            logger.info("🔄 Forçando sincronização completa...")
            
            with transaction.atomic():
                cls._check_missing_profiles()
                cls._check_premium_inconsistencies()
                cls._check_expired_subscriptions()
                cls._check_data_integrity()
            
            logger.info("✅ Sincronização forçada concluída")
            
        except Exception as e:
            logger.error(f"Erro na sincronização forçada: {e}")

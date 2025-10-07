"""
Signals para sincronização automática de pagamentos
Executa sincronização sempre que dados relevantes são modificados
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento
from home.models import Profile
from django.utils import timezone
import logging
import threading

logger = logging.getLogger(__name__)

class AutoSyncManager:
    """
    Gerenciador de sincronização automática
    Evita múltiplas sincronizações simultâneas
    """
    _sync_in_progress = False
    _sync_lock = threading.Lock()
    
    @classmethod
    def sync_user_premium_status(cls, user):
        """
        Sincroniza status premium de um usuário específico
        """
        with cls._sync_lock:
            if cls._sync_in_progress:
                return
            
            cls._sync_in_progress = True
            
            try:
                cls._perform_user_sync(user)
            finally:
                cls._sync_in_progress = False
    
    @classmethod
    def _perform_user_sync(cls, user):
        """
        Executa sincronização para um usuário
        """
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
                
                logger.info(f"🔄 Auto-sync: {user.username} -> {'Premium' if deve_ter_premium else 'Básico'}")
        
        except Exception as e:
            logger.error(f"Erro na auto-sincronização de {user.username}: {e}")

# =====================================================
# SIGNAL HANDLERS
# =====================================================

@receiver(post_save, sender=Assinatura)
def sync_on_assinatura_change(sender, instance, created, **kwargs):
    """
    Sincroniza automaticamente quando assinatura é criada/atualizada
    """
    try:
        AutoSyncManager.sync_user_premium_status(instance.usuario)
        logger.info(f"🔄 Auto-sync disparado por mudança na assinatura {instance.id}")
    except Exception as e:
        logger.error(f"Erro no signal de assinatura: {e}")

@receiver(post_delete, sender=Assinatura)
def sync_on_assinatura_delete(sender, instance, **kwargs):
    """
    Sincroniza automaticamente quando assinatura é deletada
    """
    try:
        AutoSyncManager.sync_user_premium_status(instance.usuario)
        logger.info(f"🔄 Auto-sync disparado por exclusão da assinatura {instance.id}")
    except Exception as e:
        logger.error(f"Erro no signal de exclusão de assinatura: {e}")

@receiver(post_save, sender=Pagamento)
def sync_on_pagamento_change(sender, instance, created, **kwargs):
    """
    Sincroniza automaticamente quando pagamento é criado/atualizado
    """
    try:
        # Só sincronizar se o status mudou para 'approved'
        if instance.status == 'approved':
            AutoSyncManager.sync_user_premium_status(instance.usuario)
            logger.info(f"🔄 Auto-sync disparado por pagamento aprovado {instance.id}")
    except Exception as e:
        logger.error(f"Erro no signal de pagamento: {e}")

@receiver(post_save, sender=User)
def sync_on_user_change(sender, instance, created, **kwargs):
    """
    Sincroniza automaticamente quando usuário é criado/atualizado
    """
    try:
        if created:
            # Criar perfil automaticamente para novos usuários
            Profile.objects.get_or_create(
                user=instance,
                defaults={
                    'nome': instance.username,
                    'idade': 18,
                    'faixa': 'branca'
                }
            )
            logger.info(f"🔄 Perfil criado automaticamente para {instance.username}")
        else:
            # Sincronizar usuário existente
            AutoSyncManager.sync_user_premium_status(instance)
    except Exception as e:
        logger.error(f"Erro no signal de usuário: {e}")

# =====================================================
# SISTEMA DE SINCRONIZAÇÃO PERIÓDICA
# =====================================================

class PeriodicSyncManager:
    """
    Gerenciador de sincronização periódica
    Executa sincronização automática em intervalos regulares
    """
    
    @classmethod
    def start_periodic_sync(cls):
        """
        Inicia sincronização periódica em background
        """
        def periodic_sync():
            import time
            while True:
                try:
                    # Aguardar 1 hora (3600 segundos)
                    time.sleep(3600)
                    
                    logger.info("🔄 Iniciando sincronização periódica...")
                    cls._perform_periodic_sync()
                    
                except Exception as e:
                    logger.error(f"Erro na sincronização periódica: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=periodic_sync, daemon=True)
        thread.start()
        logger.info("🔄 Sincronização periódica iniciada (intervalo: 1 hora)")
    
    @classmethod
    def _perform_periodic_sync(cls):
        """
        Executa sincronização periódica
        """
        try:
            # Corrigir assinaturas expiradas
            assinaturas_expiradas = Assinatura.objects.filter(
                status='ativa',
                data_vencimento__lt=timezone.now()
            )
            
            for assinatura in assinaturas_expiradas:
                assinatura.status = 'expirada'
                assinatura.save()
                
                # Atualizar perfil
                try:
                    profile = assinatura.usuario.profile
                    profile.conta_premium = False
                    profile.data_vencimento_premium = None
                    profile.save()
                    logger.info(f"⏰ Assinatura expirada: {assinatura.usuario.username}")
                except:
                    pass
            
            logger.info("✅ Sincronização periódica concluída")
            
        except Exception as e:
            logger.error(f"Erro na sincronização periódica: {e}")

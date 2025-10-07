"""
Sistema de notificações automáticas para problemas de pagamento
"""
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento
from home.models import Profile
from django.utils import timezone

logger = logging.getLogger(__name__)

class AutoNotificationManager:
    """
    Gerenciador de notificações automáticas
    """
    
    @classmethod
    def send_system_health_report(cls):
        """
        Envia relatório de saúde do sistema
        """
        try:
            # Coletar estatísticas
            stats = cls._collect_system_stats()
            
            # Verificar se há problemas
            problems = cls._detect_problems(stats)
            
            if problems:
                cls._send_problem_notification(problems, stats)
            else:
                cls._send_health_report(stats)
                
        except Exception as e:
            logger.error(f"Erro ao enviar relatório de saúde: {e}")
    
    @classmethod
    def _collect_system_stats(cls):
        """Coleta estatísticas do sistema"""
        try:
            return {
                'total_usuarios': User.objects.count(),
                'total_assinaturas': Assinatura.objects.count(),
                'assinaturas_ativas': Assinatura.objects.filter(
                    status='ativa',
                    data_vencimento__gt=timezone.now()
                ).count(),
                'total_pagamentos': Pagamento.objects.count(),
                'usuarios_premium': Profile.objects.filter(conta_premium=True).count(),
                'assinaturas_expiradas': Assinatura.objects.filter(
                    status='ativa',
                    data_vencimento__lt=timezone.now()
                ).count(),
                'usuarios_sem_perfil': User.objects.filter(profile__isnull=True).count(),
            }
        except Exception as e:
            logger.error(f"Erro ao coletar estatísticas: {e}")
            return {}
    
    @classmethod
    def _detect_problems(cls, stats):
        """Detecta problemas no sistema"""
        problems = []
        
        try:
            # Verificar usuários sem perfil
            if stats.get('usuarios_sem_perfil', 0) > 0:
                problems.append(f"⚠️ {stats['usuarios_sem_perfil']} usuários sem perfil")
            
            # Verificar assinaturas expiradas não atualizadas
            if stats.get('assinaturas_expiradas', 0) > 0:
                problems.append(f"⏰ {stats['assinaturas_expiradas']} assinaturas expiradas não atualizadas")
            
            # Verificar proporção de usuários premium
            total_usuarios = stats.get('total_usuarios', 0)
            usuarios_premium = stats.get('usuarios_premium', 0)
            
            if total_usuarios > 0:
                premium_ratio = usuarios_premium / total_usuarios
                if premium_ratio > 0.8:  # Mais de 80% premium
                    problems.append(f"🔍 Alto percentual de usuários premium: {premium_ratio:.1%}")
                elif premium_ratio < 0.01 and total_usuarios > 10:  # Menos de 1% premium
                    problems.append(f"📉 Baixo percentual de usuários premium: {premium_ratio:.1%}")
            
            # Verificar inconsistências
            assinaturas_ativas = stats.get('assinaturas_ativas', 0)
            usuarios_premium = stats.get('usuarios_premium', 0)
            
            if abs(assinaturas_ativas - usuarios_premium) > 5:  # Diferença significativa
                problems.append(f"🔄 Inconsistência: {assinaturas_ativas} assinaturas ativas vs {usuarios_premium} usuários premium")
            
        except Exception as e:
            logger.error(f"Erro ao detectar problemas: {e}")
        
        return problems
    
    @classmethod
    def _send_problem_notification(cls, problems, stats):
        """Envia notificação de problemas"""
        try:
            subject = "🚨 Problemas detectados no sistema de pagamentos"
            
            message = f"""
Sistema de Pagamentos - Relatório de Problemas

PROBLEMAS DETECTADOS:
{chr(10).join(problems)}

ESTATÍSTICAS ATUAIS:
- Total de usuários: {stats.get('total_usuarios', 0)}
- Assinaturas ativas: {stats.get('assinaturas_ativas', 0)}
- Usuários premium: {stats.get('usuarios_premium', 0)}
- Total de pagamentos: {stats.get('total_pagamentos', 0)}
- Assinaturas expiradas: {stats.get('assinaturas_expiradas', 0)}
- Usuários sem perfil: {stats.get('usuarios_sem_perfil', 0)}

AÇÃO RECOMENDADA:
Execute os comandos de correção automática ou verifique os logs para mais detalhes.

Sistema: Dojo-On
Data: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}
            """
            
            # Enviar email apenas se configurado
            if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER],  # Enviar para o admin
                    fail_silently=True
                )
                logger.info("📧 Notificação de problemas enviada por email")
            else:
                logger.warning("📧 Email não configurado - notificação apenas no log")
            
            # Log do problema
            logger.warning(f"🚨 Problemas detectados: {len(problems)} problemas")
            for problem in problems:
                logger.warning(f"  {problem}")
                
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de problemas: {e}")
    
    @classmethod
    def _send_health_report(cls, stats):
        """Envia relatório de saúde normal"""
        try:
            logger.info("✅ Sistema de pagamentos funcionando normalmente")
            logger.info(f"📊 Estatísticas: {stats.get('total_usuarios', 0)} usuários, {stats.get('usuarios_premium', 0)} premium")
            
        except Exception as e:
            logger.error(f"Erro ao enviar relatório de saúde: {e}")
    
    @classmethod
    def notify_payment_issue(cls, user, issue_type, details):
        """
        Notifica sobre problemas específicos de pagamento
        """
        try:
            subject = f"🔍 Problema de pagamento detectado: {issue_type}"
            
            message = f"""
Problema de Pagamento Detectado

Usuário: {user.username} ({user.email})
Tipo: {issue_type}
Detalhes: {details}
Data: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}

O sistema tentará corrigir automaticamente.
            """
            
            # Log do problema
            logger.warning(f"🔍 Problema de pagamento: {user.username} - {issue_type}")
            logger.warning(f"  Detalhes: {details}")
            
        except Exception as e:
            logger.error(f"Erro ao notificar problema de pagamento: {e}")

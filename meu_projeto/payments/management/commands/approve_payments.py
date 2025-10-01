"""
Comando para aprovar pagamentos pendentes (para teste)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Pagamento, Assinatura, PlanoPremium
from payments.views import ativar_assinatura
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Aprova pagamentos pendentes para teste'

    def add_arguments(self, parser):
        parser.add_argument('--user-id', type=int, help='ID do usuário')
        parser.add_argument('--all', action='store_true', help='Aprovar todos os pagamentos pendentes')

    def handle(self, *args, **options):
        if options.get('all'):
            # Aprovar todos os pagamentos pendentes
            pagamentos_pendentes = Pagamento.objects.filter(status='pending')
            self.stdout.write(f'Encontrados {pagamentos_pendentes.count()} pagamentos pendentes')
            
            for pagamento in pagamentos_pendentes:
                self.approve_payment(pagamento)
        elif options.get('user_id'):
            # Aprovar pagamentos de um usuário específico
            user_id = options['user_id']
            try:
                user = User.objects.get(id=user_id)
                pagamentos = Pagamento.objects.filter(usuario=user, status='pending')
                self.stdout.write(f'Encontrados {pagamentos.count()} pagamentos pendentes para {user.username}')
                
                for pagamento in pagamentos:
                    self.approve_payment(pagamento)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Usuário com ID {user_id} não encontrado'))
        else:
            self.stdout.write('Use --all para aprovar todos ou --user-id ID para um usuário específico')

    def approve_payment(self, pagamento):
        try:
            # Atualizar status do pagamento
            pagamento.status = 'approved'
            pagamento.data_pagamento = datetime.now()
            pagamento.save()
            
            self.stdout.write(f'✅ Pagamento {pagamento.id} aprovado para {pagamento.usuario.username}')
            
            # Simular dados do Mercado Pago
            payment_data = {
                'id': f'payment_{pagamento.id}',
                'status': 'approved',
                'payment_method_id': 'credit_card'
            }
            
            # Ativar assinatura
            ativar_assinatura(pagamento, payment_data)
            
            self.stdout.write(f'✅ Assinatura ativada para {pagamento.usuario.username}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao aprovar pagamento {pagamento.id}: {e}'))






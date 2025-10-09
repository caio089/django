from django.core.management.base import BaseCommand
from payments.models import PlanoPremium, Assinatura, Pagamento
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sincroniza pagamentos pendentes e cria assinaturas correspondentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa sem fazer alterações no banco de dados',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 MODO DRY-RUN - Nenhuma alteração será feita'))
        
        self.stdout.write('🔄 Iniciando sincronização de assinaturas...')
        
        # Buscar todos os pagamentos pendentes
        pagamentos_pendentes = Pagamento.objects.filter(status='pending')
        
        if not pagamentos_pendentes:
            self.stdout.write(self.style.SUCCESS('✅ Nenhum pagamento pendente encontrado!'))
            return
        
        self.stdout.write(f'🔍 Encontrados {pagamentos_pendentes.count()} pagamentos pendentes')
        
        assinaturas_criadas = 0
        pagamentos_atualizados = 0
        
        for pagamento in pagamentos_pendentes:
            self.stdout.write(f'📝 Processando pagamento ID {pagamento.id}...')
            self.stdout.write(f'   Usuário: {pagamento.usuario.username}')
            self.stdout.write(f'   Valor: R$ {pagamento.valor}')
            
            # Verificar se já existe assinatura
            assinatura_existente = Assinatura.objects.filter(
                external_reference=pagamento.external_reference
            ).first()
            
            if assinatura_existente:
                self.stdout.write(f'   ⚠️ Assinatura já existe (ID: {assinatura_existente.id})')
                continue
            
            # Buscar plano pelo valor
            plano = PlanoPremium.objects.filter(
                preco=pagamento.valor, 
                ativo=True
            ).first()
            
            if not plano:
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Plano não encontrado para valor R$ {pagamento.valor}')
                )
                continue
            
            self.stdout.write(f'   ✅ Plano encontrado: {plano.nome}')
            
            if not dry_run:
                # Calcular datas
                data_inicio = timezone.now()
                data_vencimento = data_inicio + timedelta(days=plano.duracao_dias)
                
                # Criar assinatura
                try:
                    assinatura = Assinatura.objects.create(
                        usuario=pagamento.usuario,
                        plano=plano,
                        status='ativa',
                        data_inicio=data_inicio,
                        data_vencimento=data_vencimento,
                        external_reference=pagamento.external_reference,
                        subscription_id=pagamento.payment_id
                    )
                    
                    # Atualizar pagamento
                    pagamento.status = 'approved'
                    pagamento.data_pagamento = data_inicio
                    pagamento.assinatura = assinatura
                    pagamento.save()
                    
                    assinaturas_criadas += 1
                    pagamentos_atualizados += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'   ✅ Assinatura criada com sucesso (ID: {assinatura.id})')
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'   ✅ Pagamento atualizado para "approved"')
                    )
                    self.stdout.write(f'   📅 Vencimento: {data_vencimento.strftime("%d/%m/%Y")}')
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'   ❌ Erro ao criar assinatura: {e}')
                    )
            else:
                self.stdout.write('   🔍 [DRY-RUN] Assinatura seria criada')
                assinaturas_criadas += 1
                pagamentos_atualizados += 1
        
        # Verificação final
        if not dry_run:
            assinaturas_ativas = Assinatura.objects.filter(
                status='ativa',
                data_vencimento__gt=timezone.now()
            )
            
            self.stdout.write('\n=== RESULTADO FINAL ===')
            self.stdout.write(
                self.style.SUCCESS(f'📊 Assinaturas ativas: {assinaturas_ativas.count()}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'💰 Pagamentos aprovados: {Pagamento.objects.filter(status="approved").count()}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'⏳ Pagamentos pendentes: {Pagamento.objects.filter(status="pending").count()}')
            )
        else:
            self.stdout.write('\n=== RESULTADO DRY-RUN ===')
            self.stdout.write(f'📊 Assinaturas que seriam criadas: {assinaturas_criadas}')
            self.stdout.write(f'💰 Pagamentos que seriam atualizados: {pagamentos_atualizados}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sincronização concluída!'))

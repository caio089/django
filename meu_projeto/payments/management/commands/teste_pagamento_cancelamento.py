from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento, Assinatura
from payments.views import verificar_acesso_premium
from django.utils import timezone
from datetime import timedelta
import time
import uuid

class Command(BaseCommand):
    help = 'Testa o fluxo completo de pagamento e cancelamento'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Iniciando teste de pagamento e cancelamento...'))
        
        # Buscar usuário e plano
        usuario = User.objects.filter(is_active=True).first()
        plano = PlanoPremium.objects.filter(ativo=True).first()
        
        if not usuario or not plano:
            self.stdout.write(self.style.ERROR('❌ Usuário ou plano não encontrado'))
            return
        
        self.stdout.write(f'✅ Usuário: {usuario.email}')
        self.stdout.write(f'✅ Plano: {plano.nome} - R$ {plano.preco}')
        
        # 1. VERIFICAR ACESSO ANTES DO PAGAMENTO
        self.stdout.write(self.style.WARNING('\n🔍 1. VERIFICANDO ACESSO ANTES DO PAGAMENTO...'))
        tem_acesso, assinatura = verificar_acesso_premium(usuario)
        self.stdout.write(f'   Acesso Premium: {"✅ SIM" if tem_acesso else "❌ NÃO"}')
        if assinatura:
            self.stdout.write(f'   Assinatura: {assinatura.plano.nome} - Status: {assinatura.status}')
            self.stdout.write(f'   Vencimento: {assinatura.data_vencimento.strftime("%d/%m/%Y")}')
        
        # 2. CRIAR PAGAMENTO DE TESTE
        self.stdout.write(self.style.WARNING('\n💳 2. CRIANDO PAGAMENTO DE TESTE...'))
        pagamento = Pagamento.objects.create(
            usuario=usuario,
            valor=plano.preco,
            tipo='assinatura',
            descricao=f"Teste Pagamento - {plano.nome}",
            payment_id=f'teste-pagamento-{int(time.time())}',
            status='pending'
        )
        self.stdout.write(f'   ✅ Pagamento criado: ID {pagamento.id}')
        
        # 3. SIMULAR PAGAMENTO APROVADO
        self.stdout.write(self.style.WARNING('\n✅ 3. SIMULANDO PAGAMENTO APROVADO...'))
        pagamento.status = 'approved'
        pagamento.save()
        self.stdout.write('   ✅ Pagamento aprovado')
        
        # 4. CRIAR ASSINATURA
        self.stdout.write(self.style.WARNING('\n📋 4. CRIANDO ASSINATURA...'))
        # Buscar assinatura existente ou criar nova
        assinatura = Assinatura.objects.filter(
            usuario=usuario,
            plano=plano
        ).first()
        
        if assinatura:
            # Atualizar assinatura existente
            assinatura.data_vencimento = timezone.now() + timedelta(days=30)
            assinatura.status = 'ativa'
            assinatura.external_reference = str(uuid.uuid4())
            assinatura.save()
            created = False
        else:
            # Criar nova assinatura
            assinatura = Assinatura.objects.create(
                usuario=usuario,
                plano=plano,
                data_inicio=timezone.now(),
                data_vencimento=timezone.now() + timedelta(days=30),
                status='ativa',
                external_reference=str(uuid.uuid4())
            )
            created = True
        
        if created:
            self.stdout.write('   ✅ Assinatura criada')
        else:
            self.stdout.write('   ✅ Assinatura atualizada')
        
        self.stdout.write(f'   Plano: {assinatura.plano.nome}')
        self.stdout.write(f'   Status: {assinatura.status}')
        self.stdout.write(f'   Vencimento: {assinatura.data_vencimento.strftime("%d/%m/%Y")}')
        
        # 5. VERIFICAR ACESSO APÓS PAGAMENTO
        self.stdout.write(self.style.WARNING('\n🔍 5. VERIFICANDO ACESSO APÓS PAGAMENTO...'))
        tem_acesso, assinatura = verificar_acesso_premium(usuario)
        self.stdout.write(f'   Acesso Premium: {"✅ SIM" if tem_acesso else "❌ NÃO"}')
        if assinatura:
            self.stdout.write(f'   Assinatura: {assinatura.plano.nome} - Status: {assinatura.status}')
            self.stdout.write(f'   Vencimento: {assinatura.data_vencimento.strftime("%d/%m/%Y")}')
        
        # 6. SIMULAR CANCELAMENTO
        self.stdout.write(self.style.WARNING('\n❌ 6. SIMULANDO CANCELAMENTO...'))
        assinatura.status = 'cancelada'
        assinatura.data_cancelamento = timezone.now()
        assinatura.save()
        self.stdout.write('   ✅ Assinatura cancelada')
        
        # 7. VERIFICAR ACESSO APÓS CANCELAMENTO
        self.stdout.write(self.style.WARNING('\n🔍 7. VERIFICANDO ACESSO APÓS CANCELAMENTO...'))
        tem_acesso, assinatura = verificar_acesso_premium(usuario)
        self.stdout.write(f'   Acesso Premium: {"✅ SIM" if tem_acesso else "❌ NÃO"}')
        if assinatura:
            self.stdout.write(f'   Assinatura: {assinatura.plano.nome} - Status: {assinatura.status}')
            self.stdout.write(f'   Vencimento: {assinatura.data_vencimento.strftime("%d/%m/%Y")}')
        
        # 8. SIMULAR NOVO PAGAMENTO
        self.stdout.write(self.style.WARNING('\n💳 8. SIMULANDO NOVO PAGAMENTO...'))
        novo_pagamento = Pagamento.objects.create(
            usuario=usuario,
            valor=plano.preco,
            tipo='assinatura',
            descricao=f"Teste Novo Pagamento - {plano.nome}",
            payment_id=f'teste-novo-pagamento-{int(time.time())}',
            status='approved'
        )
        self.stdout.write(f'   ✅ Novo pagamento criado: ID {novo_pagamento.id}')
        
        # 9. CRIAR NOVA ASSINATURA
        self.stdout.write(self.style.WARNING('\n📋 9. CRIANDO NOVA ASSINATURA...'))
        nova_assinatura = Assinatura.objects.create(
            usuario=usuario,
            plano=plano,
            data_inicio=timezone.now(),
            data_vencimento=timezone.now() + timedelta(days=30),
            status='ativa',
            external_reference=str(uuid.uuid4())
        )
        self.stdout.write('   ✅ Nova assinatura criada')
        
        # 10. VERIFICAR ACESSO FINAL
        self.stdout.write(self.style.WARNING('\n🔍 10. VERIFICANDO ACESSO FINAL...'))
        tem_acesso, assinatura = verificar_acesso_premium(usuario)
        self.stdout.write(f'   Acesso Premium: {"✅ SIM" if tem_acesso else "❌ NÃO"}')
        if assinatura:
            self.stdout.write(f'   Assinatura: {assinatura.plano.nome} - Status: {assinatura.status}')
            self.stdout.write(f'   Vencimento: {assinatura.data_vencimento.strftime("%d/%m/%Y")}')
        
        # RESUMO
        self.stdout.write(self.style.SUCCESS('\n📊 RESUMO DO TESTE:'))
        self.stdout.write(f'   Pagamentos criados: {Pagamento.objects.filter(usuario=usuario).count()}')
        self.stdout.write(f'   Assinaturas criadas: {Assinatura.objects.filter(usuario=usuario).count()}')
        self.stdout.write(f'   Assinaturas ativas: {Assinatura.objects.filter(usuario=usuario, status="ativa").count()}')
        self.stdout.write(f'   Assinaturas canceladas: {Assinatura.objects.filter(usuario=usuario, status="cancelada").count()}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 TESTE CONCLUÍDO COM SUCESSO!'))
        self.stdout.write(self.style.WARNING('💡 Para testar no navegador:'))
        self.stdout.write(f'   1. Acesse: http://localhost:8000/payments/checkout/{pagamento.id}/')
        self.stdout.write('   2. Clique em "Cartão de Crédito"')
        self.stdout.write('   3. Aguarde a simulação do pagamento')
        self.stdout.write('   4. Verifique se foi redirecionado para a página de sucesso')
        self.stdout.write('   5. Teste o acesso às páginas premium')

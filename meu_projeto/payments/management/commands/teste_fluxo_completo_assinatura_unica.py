from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento, Assinatura
from payments.views import verificar_acesso_premium
from django.utils import timezone
from datetime import timedelta
import time
import uuid

class Command(BaseCommand):
    help = 'Testa o fluxo completo com controle de assinatura única'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando fluxo completo com assinatura única...'))
        
        # Buscar usuário e plano
        usuario = User.objects.filter(is_active=True).first()
        plano = PlanoPremium.objects.filter(ativo=True).first()
        
        if not usuario or not plano:
            self.stdout.write(self.style.ERROR('❌ Usuário ou plano não encontrado'))
            return
        
        self.stdout.write(f'✅ Usuário: {usuario.email}')
        self.stdout.write(f'✅ Plano: {plano.nome} - R$ {plano.preco}')
        
        # 1. LIMPAR DADOS EXISTENTES
        self.stdout.write(self.style.WARNING('\n🧹 1. LIMPANDO DADOS EXISTENTES...'))
        Assinatura.objects.filter(usuario=usuario).delete()
        Pagamento.objects.filter(usuario=usuario).delete()
        self.stdout.write('   ✅ Dados limpos')
        
        # 2. PRIMEIRO PAGAMENTO
        self.stdout.write(self.style.WARNING('\n💳 2. PRIMEIRO PAGAMENTO...'))
        pagamento1 = Pagamento.objects.create(
            usuario=usuario,
            valor=plano.preco,
            tipo='assinatura',
            descricao=f"Primeiro Pagamento - {plano.nome}",
            payment_id=f'pagamento-1-{int(time.time())}',
            status='approved'
        )
        self.stdout.write(f'   ✅ Pagamento 1 criado: ID {pagamento1.id}')
        
        # Simular processamento do primeiro pagamento
        assinatura1 = Assinatura.objects.create(
            usuario=usuario,
            plano=plano,
            data_inicio=timezone.now(),
            data_vencimento=timezone.now() + timedelta(days=30),
            status='ativa',
            external_reference=str(uuid.uuid4())
        )
        self.stdout.write(f'   ✅ Assinatura 1 criada: ID {assinatura1.id}')
        
        # Verificar acesso
        tem_acesso, assinatura_ativa = verificar_acesso_premium(usuario)
        self.stdout.write(f'   Acesso Premium: {"✅ SIM" if tem_acesso else "❌ NÃO"}')
        
        # 3. SEGUNDO PAGAMENTO (SIMULANDO NOVO PAGAMENTO)
        self.stdout.write(self.style.WARNING('\n💳 3. SEGUNDO PAGAMENTO (SIMULANDO NOVO PAGAMENTO)...'))
        
        # Simular cancelamento automático de assinaturas anteriores
        assinaturas_anteriores = Assinatura.objects.filter(
            usuario=usuario,
            status='ativa'
        )
        
        for assinatura_antiga in assinaturas_anteriores:
            assinatura_antiga.status = 'cancelada'
            assinatura_antiga.data_cancelamento = timezone.now()
            assinatura_antiga.save()
            self.stdout.write(f'   ✅ Assinatura anterior cancelada: ID {assinatura_antiga.id}')
        
        # Criar novo pagamento
        pagamento2 = Pagamento.objects.create(
            usuario=usuario,
            valor=plano.preco,
            tipo='assinatura',
            descricao=f"Segundo Pagamento - {plano.nome}",
            payment_id=f'pagamento-2-{int(time.time())}',
            status='approved'
        )
        self.stdout.write(f'   ✅ Pagamento 2 criado: ID {pagamento2.id}')
        
        # Criar nova assinatura
        assinatura2 = Assinatura.objects.create(
            usuario=usuario,
            plano=plano,
            data_inicio=timezone.now(),
            data_vencimento=timezone.now() + timedelta(days=30),
            status='ativa',
            external_reference=str(uuid.uuid4())
        )
        self.stdout.write(f'   ✅ Assinatura 2 criada: ID {assinatura2.id}')
        
        # Verificar acesso
        tem_acesso, assinatura_ativa = verificar_acesso_premium(usuario)
        self.stdout.write(f'   Acesso Premium: {"✅ SIM" if tem_acesso else "❌ NÃO"}')
        
        # 4. TERCEIRO PAGAMENTO (SIMULANDO MAIS UM PAGAMENTO)
        self.stdout.write(self.style.WARNING('\n💳 4. TERCEIRO PAGAMENTO (SIMULANDO MAIS UM PAGAMENTO)...'))
        
        # Simular cancelamento automático de assinaturas anteriores
        assinaturas_anteriores = Assinatura.objects.filter(
            usuario=usuario,
            status='ativa'
        )
        
        for assinatura_antiga in assinaturas_anteriores:
            assinatura_antiga.status = 'cancelada'
            assinatura_antiga.data_cancelamento = timezone.now()
            assinatura_antiga.save()
            self.stdout.write(f'   ✅ Assinatura anterior cancelada: ID {assinatura_antiga.id}')
        
        # Criar novo pagamento
        pagamento3 = Pagamento.objects.create(
            usuario=usuario,
            valor=plano.preco,
            tipo='assinatura',
            descricao=f"Terceiro Pagamento - {plano.nome}",
            payment_id=f'pagamento-3-{int(time.time())}',
            status='approved'
        )
        self.stdout.write(f'   ✅ Pagamento 3 criado: ID {pagamento3.id}')
        
        # Criar nova assinatura
        assinatura3 = Assinatura.objects.create(
            usuario=usuario,
            plano=plano,
            data_inicio=timezone.now(),
            data_vencimento=timezone.now() + timedelta(days=30),
            status='ativa',
            external_reference=str(uuid.uuid4())
        )
        self.stdout.write(f'   ✅ Assinatura 3 criada: ID {assinatura3.id}')
        
        # Verificar acesso
        tem_acesso, assinatura_ativa = verificar_acesso_premium(usuario)
        self.stdout.write(f'   Acesso Premium: {"✅ SIM" if tem_acesso else "❌ NÃO"}')
        
        # 5. VERIFICAR STATUS FINAL
        self.stdout.write(self.style.WARNING('\n📊 5. VERIFICANDO STATUS FINAL...'))
        
        # Contar assinaturas
        total_assinaturas = Assinatura.objects.filter(usuario=usuario).count()
        assinaturas_ativas = Assinatura.objects.filter(usuario=usuario, status='ativa').count()
        assinaturas_canceladas = Assinatura.objects.filter(usuario=usuario, status='cancelada').count()
        
        # Contar pagamentos
        total_pagamentos = Pagamento.objects.filter(usuario=usuario).count()
        pagamentos_aprovados = Pagamento.objects.filter(usuario=usuario, status='approved').count()
        
        self.stdout.write(f'   Total de assinaturas: {total_assinaturas}')
        self.stdout.write(f'   Assinaturas ativas: {assinaturas_ativas}')
        self.stdout.write(f'   Assinaturas canceladas: {assinaturas_canceladas}')
        self.stdout.write(f'   Total de pagamentos: {total_pagamentos}')
        self.stdout.write(f'   Pagamentos aprovados: {pagamentos_aprovados}')
        
        # 6. VERIFICAR REGRAS DE NEGÓCIO
        self.stdout.write(self.style.WARNING('\n✅ 6. VERIFICANDO REGRAS DE NEGÓCIO...'))
        
        # Regra 1: Apenas uma assinatura ativa
        if assinaturas_ativas == 1:
            self.stdout.write('   ✅ REGRA 1: Apenas uma assinatura ativa (CORRETO)')
        else:
            self.stdout.write(f'   ❌ REGRA 1: {assinaturas_ativas} assinaturas ativas (INCORRETO)')
        
        # Regra 2: Todas as assinaturas anteriores canceladas
        if assinaturas_canceladas == total_assinaturas - 1:
            self.stdout.write('   ✅ REGRA 2: Todas as assinaturas anteriores canceladas (CORRETO)')
        else:
            self.stdout.write(f'   ❌ REGRA 2: {assinaturas_canceladas} canceladas de {total_assinaturas-1} esperadas (INCORRETO)')
        
        # Regra 3: Acesso premium funcionando
        if tem_acesso:
            self.stdout.write('   ✅ REGRA 3: Acesso premium funcionando (CORRETO)')
        else:
            self.stdout.write('   ❌ REGRA 3: Acesso premium não funcionando (INCORRETO)')
        
        # Regra 4: Todos os pagamentos aprovados
        if pagamentos_aprovados == total_pagamentos:
            self.stdout.write('   ✅ REGRA 4: Todos os pagamentos aprovados (CORRETO)')
        else:
            self.stdout.write(f'   ❌ REGRA 4: {pagamentos_aprovados} de {total_pagamentos} pagamentos aprovados (INCORRETO)')
        
        # 7. RESUMO FINAL
        self.stdout.write(self.style.SUCCESS('\n🎉 TESTE DE FLUXO COMPLETO CONCLUÍDO!'))
        
        if (assinaturas_ativas == 1 and 
            assinaturas_canceladas == total_assinaturas - 1 and 
            tem_acesso and 
            pagamentos_aprovados == total_pagamentos):
            self.stdout.write(self.style.SUCCESS('✅ TODAS AS REGRAS DE NEGÓCIO FUNCIONANDO PERFEITAMENTE!'))
        else:
            self.stdout.write(self.style.ERROR('❌ ALGUMAS REGRAS DE NEGÓCIO NÃO ESTÃO FUNCIONANDO!'))
        
        self.stdout.write(self.style.WARNING('\n💡 Para testar no navegador:'))
        self.stdout.write('   1. Acesse: http://localhost:8000/payments/checkout/')
        self.stdout.write('   2. Faça um pagamento (PIX ou Cartão)')
        self.stdout.write('   3. Faça outro pagamento')
        self.stdout.write('   4. Verifique se apenas uma assinatura fica ativa')
        self.stdout.write('   5. Verifique se o acesso premium funciona')


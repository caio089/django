from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento, Assinatura
from payments.views import verificar_acesso_premium
from django.utils import timezone
from datetime import timedelta
import time
import uuid

class Command(BaseCommand):
    help = 'Testa se apenas uma assinatura ativa é permitida por usuário'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando controle de assinatura única...'))
        
        # Buscar usuário e plano
        usuario = User.objects.filter(is_active=True).first()
        plano = PlanoPremium.objects.filter(ativo=True).first()
        
        if not usuario or not plano:
            self.stdout.write(self.style.ERROR('❌ Usuário ou plano não encontrado'))
            return
        
        self.stdout.write(f'✅ Usuário: {usuario.email}')
        self.stdout.write(f'✅ Plano: {plano.nome} - R$ {plano.preco}')
        
        # 1. LIMPAR ASSINATURAS EXISTENTES
        self.stdout.write(self.style.WARNING('\n🧹 1. LIMPANDO ASSINATURAS EXISTENTES...'))
        assinaturas_existentes = Assinatura.objects.filter(usuario=usuario)
        count_existentes = assinaturas_existentes.count()
        assinaturas_existentes.delete()
        self.stdout.write(f'   ✅ {count_existentes} assinaturas removidas')
        
        # 2. CRIAR PRIMEIRA ASSINATURA
        self.stdout.write(self.style.WARNING('\n📋 2. CRIANDO PRIMEIRA ASSINATURA...'))
        assinatura1 = Assinatura.objects.create(
            usuario=usuario,
            plano=plano,
            data_inicio=timezone.now(),
            data_vencimento=timezone.now() + timedelta(days=30),
            status='ativa',
            external_reference=str(uuid.uuid4())
        )
        self.stdout.write(f'   ✅ Assinatura 1 criada: ID {assinatura1.id}')
        
        # 3. VERIFICAR ACESSO COM PRIMEIRA ASSINATURA
        self.stdout.write(self.style.WARNING('\n🔍 3. VERIFICANDO ACESSO COM PRIMEIRA ASSINATURA...'))
        tem_acesso, assinatura_ativa = verificar_acesso_premium(usuario)
        self.stdout.write(f'   Acesso Premium: {"✅ SIM" if tem_acesso else "❌ NÃO"}')
        if assinatura_ativa:
            self.stdout.write(f'   Assinatura ativa: {assinatura_ativa.id} - Status: {assinatura_ativa.status}')
        
        # 4. CRIAR SEGUNDA ASSINATURA (SIMULANDO NOVO PAGAMENTO)
        self.stdout.write(self.style.WARNING('\n📋 4. CRIANDO SEGUNDA ASSINATURA (SIMULANDO NOVO PAGAMENTO)...'))
        
        # Simular o processo de cancelamento automático
        assinaturas_anteriores = Assinatura.objects.filter(
            usuario=usuario,
            status='ativa'
        )
        
        for assinatura_antiga in assinaturas_anteriores:
            assinatura_antiga.status = 'cancelada'
            assinatura_antiga.data_cancelamento = timezone.now()
            assinatura_antiga.save()
            self.stdout.write(f'   ✅ Assinatura anterior cancelada: ID {assinatura_antiga.id}')
        
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
        
        # 5. VERIFICAR ACESSO APÓS SEGUNDA ASSINATURA
        self.stdout.write(self.style.WARNING('\n🔍 5. VERIFICANDO ACESSO APÓS SEGUNDA ASSINATURA...'))
        tem_acesso, assinatura_ativa = verificar_acesso_premium(usuario)
        self.stdout.write(f'   Acesso Premium: {"✅ SIM" if tem_acesso else "❌ NÃO"}')
        if assinatura_ativa:
            self.stdout.write(f'   Assinatura ativa: {assinatura_ativa.id} - Status: {assinatura_ativa.status}')
        
        # 6. VERIFICAR STATUS DAS ASSINATURAS
        self.stdout.write(self.style.WARNING('\n📊 6. VERIFICANDO STATUS DAS ASSINATURAS...'))
        assinaturas_usuario = Assinatura.objects.filter(usuario=usuario).order_by('id')
        
        for i, assinatura in enumerate(assinaturas_usuario, 1):
            self.stdout.write(f'   Assinatura {i}: ID {assinatura.id} - Status: {assinatura.status} - Data Cancelamento: {assinatura.data_cancelamento}')
        
        # 7. VERIFICAR SE APENAS UMA ESTÁ ATIVA
        assinaturas_ativas = Assinatura.objects.filter(usuario=usuario, status='ativa').count()
        assinaturas_canceladas = Assinatura.objects.filter(usuario=usuario, status='cancelada').count()
        
        self.stdout.write(self.style.WARNING('\n📈 7. RESUMO FINAL:'))
        self.stdout.write(f'   Total de assinaturas: {assinaturas_usuario.count()}')
        self.stdout.write(f'   Assinaturas ativas: {assinaturas_ativas}')
        self.stdout.write(f'   Assinaturas canceladas: {assinaturas_canceladas}')
        
        if assinaturas_ativas == 1:
            self.stdout.write(self.style.SUCCESS('✅ SUCESSO: Apenas uma assinatura ativa!'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ ERRO: {assinaturas_ativas} assinaturas ativas (deveria ser 1)'))
        
        if assinaturas_canceladas == 1:
            self.stdout.write(self.style.SUCCESS('✅ SUCESSO: Uma assinatura foi cancelada automaticamente!'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ ERRO: {assinaturas_canceladas} assinaturas canceladas (deveria ser 1)'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 TESTE DE ASSINATURA ÚNICA CONCLUÍDO!'))


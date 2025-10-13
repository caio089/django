"""
Comando para atualizar o preço do plano mensal de R$ 39,90 para R$ 49,90
"""
from django.core.management.base import BaseCommand
from payments.models import PlanoPremium
from decimal import Decimal


class Command(BaseCommand):
    help = 'Atualiza o preço do plano mensal de R$ 39,90 para R$ 49,90'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS('🔄 ATUALIZANDO PREÇO DO PLANO PREMIUM'))
        self.stdout.write("=" * 70)
        
        # Buscar planos com preço antigo (39.90)
        planos_antigos = PlanoPremium.objects.filter(preco=Decimal('39.90'))
        
        if planos_antigos.exists():
            count = planos_antigos.count()
            self.stdout.write(f"\n✅ Encontrados {count} plano(s) com preço R$ 39,90")
            
            # Atualizar para novo preço
            planos_antigos.update(preco=Decimal('49.90'))
            
            self.stdout.write(self.style.SUCCESS(f"\n✅ {count} plano(s) atualizado(s) para R$ 49,90!"))
            
            # Listar planos atualizados
            self.stdout.write("\n📋 Planos atualizados:")
            for plano in PlanoPremium.objects.filter(preco=Decimal('49.90')):
                self.stdout.write(f"   - {plano.nome}: R$ {plano.preco}")
        else:
            self.stdout.write(self.style.WARNING("\n⚠️ Nenhum plano com preço R$ 39,90 encontrado"))
            
            # Verificar se já existem planos com novo preço
            planos_novos = PlanoPremium.objects.filter(preco=Decimal('49.90'))
            if planos_novos.exists():
                self.stdout.write(self.style.SUCCESS(f"\n✅ Já existem {planos_novos.count()} plano(s) com R$ 49,90"))
                for plano in planos_novos:
                    self.stdout.write(f"   - {plano.nome}: R$ {plano.preco}")
            else:
                self.stdout.write("\n📝 Criando novo plano com R$ 49,90...")
                plano = PlanoPremium.objects.create(
                    nome="Plano Mensal Premium",
                    descricao="Acesso completo à plataforma de judô com todos os recursos premium",
                    preco=Decimal('49.90'),
                    duracao_dias=30,
                    ativo=True,
                    acesso_ilimitado_quiz=True,
                    relatorios_detalhados=True,
                    suporte_prioritario=True
                )
                self.stdout.write(self.style.SUCCESS(f"\n✅ Plano criado: {plano.nome} - R$ {plano.preco}"))
        
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS('✅ ATUALIZAÇÃO CONCLUÍDA!'))
        self.stdout.write("=" * 70)
        self.stdout.write("")


"""
Comando de gerenciamento Django para atualizar o preço dos planos
"""
from django.core.management.base import BaseCommand
from payments.models import PlanoPremium


class Command(BaseCommand):
    help = 'Atualiza o preço dos planos de R$ 49,90 para R$ 29,90'

    def handle(self, *args, **options):
        """
        Atualiza todos os planos com preço 49.90 para 29.90
        """
        try:
            # Buscar planos com preço 49.90
            planos_antigos = PlanoPremium.objects.filter(preco=49.90)
            
            if not planos_antigos.exists():
                self.stdout.write(
                    self.style.WARNING('Nenhum plano com preço R$ 49,90 encontrado.')
                )
                return
            
            # Atualizar preços
            planos_atualizados = planos_antigos.update(preco=29.90)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ {planos_atualizados} plano(s) atualizado(s) com sucesso!'
                )
            )
            
            # Mostrar detalhes dos planos atualizados
            for plano in planos_antigos:
                self.stdout.write(
                    f'  - {plano.nome}: R$ 49,90 → R$ 29,90'
                )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao atualizar planos: {e}')
            )
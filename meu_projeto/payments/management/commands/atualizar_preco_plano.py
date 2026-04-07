"""Comando para padronizar os preços dos planos ativos."""
from django.core.management.base import BaseCommand
from payments.models import PlanoPremium


class Command(BaseCommand):
    help = 'Padroniza preços: Mensal R$ 47,90 e Trimestral R$ 119,90'

    def handle(self, *args, **options):
        """Mantém apenas preços oficiais para mensal/trimestral."""
        try:
            mensal_qs = PlanoPremium.objects.filter(ativo=True, duracao_dias=30)
            trimestral_qs = PlanoPremium.objects.filter(ativo=True, duracao_dias=90)

            mensal_count = mensal_qs.update(preco=47.90)
            trimestral_count = trimestral_qs.update(preco=119.90)

            self.stdout.write(self.style.SUCCESS('Preços padronizados com sucesso:'))
            self.stdout.write(f'  - Mensal atualizado(s): {mensal_count} -> R$ 47,90')
            self.stdout.write(f'  - Trimestral atualizado(s): {trimestral_count} -> R$ 119,90')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao atualizar planos: {e}')
            )
from django.db import models


class DashboardFinanceSettings(models.Model):
    """
    Configurações financeiras editáveis pelo admin.

    - revenue_offset: permite "zerar" a métrica de receita total sem apagar pagamentos.
      Receita exibida = receita_aprovada_total - revenue_offset (nunca abaixo de 0).
    - infra_cost / additional_cost: custos informados manualmente pelo admin.
    """

    revenue_offset = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    infra_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    additional_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuração financeira do dashboard"
        verbose_name_plural = "Configurações financeiras do dashboard"

    def __str__(self):
        return f"FinanceSettings(id={self.id})"

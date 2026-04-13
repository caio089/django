from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DashboardFinanceSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("revenue_offset", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("infra_cost", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("additional_cost", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Configuração financeira do dashboard",
                "verbose_name_plural": "Configurações financeiras do dashboard",
            },
        ),
    ]


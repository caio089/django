from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0009_pagamento_admin_notification_fields"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="assinatura",
            index=models.Index(fields=["status", "data_vencimento"], name="assin_status_venc_idx"),
        ),
        migrations.AddIndex(
            model_name="pagamento",
            index=models.Index(fields=["status", "data_criacao"], name="pag_status_cria_idx"),
        ),
        migrations.AddIndex(
            model_name="webhookevent",
            index=models.Index(fields=["data_recebimento"], name="wh_received_idx"),
        ),
    ]


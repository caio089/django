from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0008_alter_planopremium_imagem_1_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pagamento",
            name="admin_notification_sent",
            field=models.BooleanField(default=False, verbose_name="Notificação admin enviada"),
        ),
        migrations.AddField(
            model_name="pagamento",
            name="admin_notification_sent_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Data notificação admin"),
        ),
    ]


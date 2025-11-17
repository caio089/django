from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_codigorecuperacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='trial_inicio',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Início do período grátis'),
        ),
        migrations.AddField(
            model_name='profile',
            name='trial_fim',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Fim do período grátis'),
        ),
    ]






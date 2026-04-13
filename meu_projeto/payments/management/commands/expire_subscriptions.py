from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from payments.models import Assinatura
from home.models import Profile


class Command(BaseCommand):
    help = "Expira assinaturas vencidas e sincroniza Profile em lote (ideal para cron no Render)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mostra quantas assinaturas seriam expiradas sem alterar o banco.",
        )

    def handle(self, *args, **options):
        dry_run = bool(options.get("dry_run"))
        now = timezone.now()

        vencidas_qs = Assinatura.objects.filter(status="ativa", data_vencimento__lt=now)
        vencidas_count = vencidas_qs.count()

        if dry_run:
            self.stdout.write(self.style.WARNING("🔍 DRY-RUN (nenhuma alteração será feita)"))
            self.stdout.write(f"Assinaturas vencidas: {vencidas_count}")
            return

        if vencidas_count == 0:
            self.stdout.write(self.style.SUCCESS("✅ Nenhuma assinatura vencida para expirar."))
            return

        with transaction.atomic():
            user_ids = list(vencidas_qs.values_list("usuario_id", flat=True).distinct())
            vencidas_qs.update(status="expirada", ativo=False)

            # Atualizar Profile apenas dos usuários afetados
            Profile.objects.filter(user_id__in=user_ids).update(
                conta_premium=False,
                data_vencimento_premium=None,
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Assinaturas expiradas: {vencidas_count}"))


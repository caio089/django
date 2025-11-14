from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Profile
from .trial import trial_delta


@receiver(post_save, sender=User)
def ensure_profile_and_trial(sender, instance: User, created: bool, **kwargs):
    """
    Garante que todo usuário recém-criado tenha Profile e trial ativo.
    """
    try:
        if created:
            profile, _ = Profile.objects.get_or_create(
                user=instance,
                defaults={
                    'nome': instance.get_full_name() or instance.username or (instance.email if hasattr(instance, 'email') else 'Usuário'),
                    'idade': 18,
                    'faixa': 'branca',
                },
            )
            if not profile.trial_inicio:
                now = timezone.now()
                profile.trial_inicio = now
                profile.trial_fim = now + trial_delta()
                profile.save(update_fields=['trial_inicio', 'trial_fim'])
                print(f"[signals] Trial iniciado no cadastro. user_id={instance.id} inicio={profile.trial_inicio} fim={profile.trial_fim}")
        else:
            # Se já existia e ainda não tem trial, iniciar
            try:
                profile = instance.profile
                if not profile.trial_inicio:
                    now = timezone.now()
                    profile.trial_inicio = now
                    profile.trial_fim = now + trial_delta()
                    profile.save(update_fields=['trial_inicio', 'trial_fim'])
                    print(f"[signals] Trial iniciado (profile sem trial). user_id={instance.id} inicio={profile.trial_inicio} fim={profile.trial_fim}")
            except Profile.DoesNotExist:
                # Cria profile e trial
                profile = Profile.objects.create(
                    user=instance,
                    nome=instance.get_full_name() or instance.username or (instance.email if hasattr(instance, 'email') else 'Usuário'),
                    idade=18,
                    faixa='branca',
                )
                now = timezone.now()
                profile.trial_inicio = now
                profile.trial_fim = now + trial_delta()
                profile.save(update_fields=['trial_inicio', 'trial_fim'])
                print(f"[signals] Profile criado + trial (sem profile). user_id={instance.id} inicio={profile.trial_inicio} fim={profile.trial_fim}")
    except Exception as e:
        print(f"[signals] ERRO ao garantir trial no cadastro: user_id={instance.id} err={e}")




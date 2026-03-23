from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def ensure_profile(sender, instance: User, created: bool, **kwargs):
    """Garante que todo usuário tenha Profile (sem trial)."""
    try:
        Profile.objects.get_or_create(
            user=instance,
            defaults={
                'nome': instance.get_full_name() or instance.username or (instance.email if hasattr(instance, 'email') else 'Usuário'),
                'idade': 18,
                'faixa': 'branca',
            },
        )
    except Exception:
        pass




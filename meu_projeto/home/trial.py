from datetime import timedelta
from django.conf import settings


def trial_delta() -> timedelta:
	"""
	Retorna o timedelta do período de teste.
	Pode ser sobrescrito por TRIAL_SECONDS_OVERRIDE (para testes).
	"""
	seconds_override = getattr(settings, 'TRIAL_SECONDS_OVERRIDE', 0) or 0
	if seconds_override and int(seconds_override) > 0:
		return timedelta(seconds=int(seconds_override))
	
	days = getattr(settings, 'TRIAL_DAYS', 3) or 3
	return timedelta(days=int(days))



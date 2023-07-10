from django.apps import AppConfig

from accounts.signals import user_registration_signal


class ScoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scoring'

    def ready(self):
        from .signals.handlers import create_player_profile
        user_registration_signal.connect(create_player_profile)

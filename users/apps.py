from django.apps import AppConfig
from django.db.models.signals import post_save
from django.core.signals import request_started


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Usuarios'

    def ready(self):
        from django.contrib.auth.models import User
        from users.models import UserProfile
        from users.signals import (
            create_user_profile, warm_user_profile_avatar, force_language
        )

        post_save.connect(create_user_profile, sender=User)
        post_save.connect(warm_user_profile_avatar, sender=UserProfile)
        request_started.connect(force_language)

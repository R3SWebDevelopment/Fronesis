from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Usuarios'

    def ready(self):
        from django.contrib.auth.models import User
        from users.models import UserProfile
        from users.signals import (
            create_user_profile, warm_user_profile_avatar,
        )

        post_save.connect(create_user_profile, sender=User)
        post_save.connect(warm_user_profile_avatar, sender=UserProfile)

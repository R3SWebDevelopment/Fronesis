from drum.links.models import Profile
from django.db import models


class UserProfile(Profile):
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.user, self.karma)

from versatileimagefield.fields import VersatileImageField
from drum.links.models import Profile


class UserProfile(Profile):
    avatar = VersatileImageField(null=True, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.user, self.karma)

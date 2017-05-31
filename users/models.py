from versatileimagefield.fields import VersatileImageField, PPOIField
from drum.links.models import Profile


class UserProfile(Profile):
    avatar = VersatileImageField(null=True, blank=True, ppoi_field='ppoi', upload_to='images/avatars/',)
    ppoi = PPOIField('Image PPOI', default=(0.5, 0.5))

    def __str__(self):
        return '{} ({})'.format(self.user, self.karma)

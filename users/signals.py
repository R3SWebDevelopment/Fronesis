from .models import UserProfile
from drum.links.models import Profile


def create_user_profile(sender, **kwargs):
    u = kwargs['instance']
    p = Profile.objects.filter(user=u)

    if p.exists():
        p = p.first()
        up = UserProfile.objects.filter(profile_ptr=p)

        if not up.exists():
            up = UserProfile(profile_ptr_id=p.pk)
            up.__dict__.update(p.__dict__)
            up.save()
    else:
        UserProfile.objects.create(user=u)

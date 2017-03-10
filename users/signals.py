from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from drum.links.models import Profile
from .models import UserProfile


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


def warm_user_profile_avatar(sender, **kwargs):
    i = kwargs['instance']

    img_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=i,
        rendition_key_set='userprofile_avatar',
        image_attr='avatar'
    )

    num_created, failed_to_create = img_warmer.warm()
    print('Avatar images create: {}, {}'.format(num_created, failed_to_create))

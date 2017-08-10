from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from django.db.models.signals import post_save
from drum.links.models import Profile
from .models import UserProfile
from .tasks import notify_user_creation

def force_language(sender, environ, **kwargs):
    from django.utils import translation
    translation.activate('en-us')
    environ.update({
        'HTTP_ACCEPT_LANGUAGE': translation.get_language()
    })

def create_user_profile(sender, **kwargs):
    # When an user is created verify if has password if not generate a random one and send it.
    # any case notify the user that he has join the plataform
    if kwargs.get('created', False):
        user = kwargs['instance']
        random_password = None
        if user.password is None or len(user.password.strip()) == 0:
            random_password = user.__class__.objects.make_random_password()
            # Disconnect signal to avoid transaction abortion
            post_save.disconnect(receiver=create_user_profile, sender=sender)
            user.set_password(random_password)
            user.save()
            # reconnect the signal
            post_save.connect(create_user_profile, sender=sender)
        notify_user_creation.apply_async(kwargs={
            'user_id': user.id,
            'random_password': random_password
        })

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

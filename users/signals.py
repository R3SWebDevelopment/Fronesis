from .models import UserProfile


def create_user_profile(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']

    if created:
        UserProfile.objects.create(user=instance)


def save_user_profile(sender, **kwargs):
    instance = kwargs['instance']

    instance.userprofile.save()

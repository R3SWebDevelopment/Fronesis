from django.contrib.auth.models import User


def get_logged_user(request):
    user = request.user
    try:
        return User.objects.get(pk=user.pk)
    except User.DoesNotExist:
        return None


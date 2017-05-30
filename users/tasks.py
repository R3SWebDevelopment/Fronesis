# Create your tasks here
from __future__ import absolute_import, unicode_literals
import celery
from utils.utils import send_email
from django.contrib.auth.models import User


@celery.task(name='events.tickets.reservation.check')
def notify_user_creation(user_id, random_password):
    try:
        user = User.objects.get(id=user_id)
        template_file = 'users/signup-notification.html'
        context_data = {
            'username': user.email,
            'name': user.get_full_name(),
            'password': random_password,
        }
        subject = 'Fronesis would like to welcome you'
        recepiants = [
            user.email
        ]
        send_email(template_file=template_file, context_data=context_data, subject=subject, recepiants=recepiants)
    except User.DoesNotExist:
        pass



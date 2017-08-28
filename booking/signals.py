from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib.contenttypes.models import ContentType
import os


def create_appointment(sender, *args, **kwargs):
    if kwargs.get('created', False):
        appointment = kwargs.get('instance', None)

        payment_url = ''

        if not appointment.already_paid:
            payment_info = appointment.generate_payment_info()



        data = {
            'appointment': appointment
        }
        subject = 'Appointment with {} at {} for {}'.format(appointment.coach.get_full_name, appointment.venue_name,
                                                            appointment.service_name)
        to_email = [appointment.client.email]
        from_email = os.environ.get("DEFAULT_FROM_EMAIL")
        message = get_template('project_invitation.html').render(data)
        msg = EmailMultiAlternatives(subject, message, to=to_email, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()



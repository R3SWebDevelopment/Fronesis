from django.db import models
from coaches.models import Coach, Venue, Client, Session
from dateutil import tz
from django.contrib.contenttypes.models import ContentType

LOCAL = tz.gettz('America/Monterrey')


class Appointments(models.Model):
    coach = models.ForeignKey(Coach, null=False, related_name='appointments')
    starts_datetime = models.DateTimeField(null=True)
    ends_datetime = models.DateTimeField(null=True)
    online_call = models.BooleanField(default=False)
    custome_venue = models.TextField(null=True)
    venue = models.ForeignKey(Venue, null=True, related_name='appointments')
    client = models.ForeignKey(Client, null=False, related_name='appointments')
    service = models.ForeignKey(Session, null=True, related_name='appointments')
    already_paid = models.BooleanField(default=False)
    send_payment_link = models.BooleanField(default=False)
    google_calendar_url = models.URLField(null=True)

    @property
    def venue_name(self):
        return self.venue.name if self.venue else self.custome_venue

    @property
    def service_name(self):
        return self.service.name

    @property
    def client_name(self):
        return self.client.full_name or self.client.email

    @property
    def summary(self):
        return '{} with {}'.format(self.service_name, self.client_name)

    @property
    def location(self):
        return '{} - {}'.format(self.venue.name, self.venue.address) \
            if self.venue else self.custome_venue \
            if self.custome_venue else 'No Location info'

    @property
    def starts_datetime_local(self):
        return self.starts_datetime.astimezone(LOCAL)

    @property
    def ends_datetime_local(self):
        return self.ends_datetime.astimezone(LOCAL)

    @property
    def start(self):
        return {
            'dateTime': self.starts_datetime.astimezone(LOCAL).strftime('%Y-%m-%dT%H:%M:%S%z')
        }

    @property
    def end(self):
        return {
            'dateTime': self.ends_datetime.astimezone(LOCAL).strftime('%Y-%m-%dT%H:%M:%S%z')
        }

    @property
    def attendees(self):
        return [
            {
                'email': self.coach.user.email,
                'displayName': self.coach.user.get_full_name() or self.coach.user.email,
            },
            {
                'email': self.client.email,
                'displayName': self.client.full_name,
            },
        ]

    @property
    def amount(self):
        return self.service.price

    @property
    def google_calendar_data(self):
        data = {
            'summary': self.summary,
            'start': self.start,
            'end': self.end,
            'attendees': self.attendees,
            'sendNotifications': True,
            'location': self.location,
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        return data

    @property
    def payment_info(self):
        content_type = ContentType.objects.get_for_model(self)
        return ServicePayment.objects.filter(service_content_type=content_type, service_object_pk=self.pk).first()

    def generate_payment_info(self):
        content_type = ContentType.objects.get_for_model(self)
        instance, created = ServicePayment.objects.get_or_create(service_content_type=content_type,
                                                                 service_object_pk=self.pk, amount=self.amount)
        return instance


class AppointmentRequest(models.Model):
    coach = models.ForeignKey(Coach, null=False, related_name='appointments_request')
    starts_datetime = models.DateTimeField(null=True)
    ends_datetime = models.DateTimeField(null=True)
    online_call = models.BooleanField(default=False)
    venue = models.ForeignKey(Venue, null=True, related_name='appointments_request')
    client = models.ForeignKey(Client, null=False, related_name='appointments_request')
    service = models.ForeignKey(Session, null=True, related_name='appointments_request')

    @property
    def is_available(self):
        appointments = self.coach.appointments.exclude(starts_datetime__gte=self.ends_datetime).\
            exclude(ends_datetime__lte=self.starts_datetime)
        if appointments.exists():
            return False
        return True


class ServicePayment(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    credit_card = models.CharField(max_length=16, null=True)
    auth_number = models.CharField(max_length=16, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    processed_timestamp = models.DateTimeField()
    service_content_type = models.ForeignKey(ContentType, null=True)
    service_object_pk = models.IntegerField(null=True)

    @property
    def service(self):
        return self.service_content_type.model_class.objects.filter(pk=self.service_object_pk).first()


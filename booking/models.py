from django.db import models
from coaches.models import Coach, Venue, Client, Session
from dateutil import tz

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
    google_calender_url = models.URLField(null=True)

    @property
    def venue_name(self):
        return self.venue.name if self.venue else self.custome_venue

    @property
    def service_name(self):
        return self.service.name

    @property
    def client_name(self):
        return self.client.full_name

    @property
    def summary(self):
        return '{} with {}'.format(self.service_name, self.client_name)

    @property
    def location(self):
        return '{} - {}'.format(self.venue.name, self.venue.address) \
            if self.venue else self.custome_venue \
            if self.custome_venue else 'No Location info'

    @property
    def start(self):
        return {
            'dateTime': self.starts_datetime.replace(tzinfo=LOCAL).strftime('%Y-%m-%dT%H:%M:%S%z')
        }

    @property
    def end(self):
        return {
            'dateTime': self.ends_datetime.replace(tzinfo=LOCAL).strftime('%Y-%m-%dT%H:%M:%S%z')
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

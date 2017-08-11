from django.db import models
from coaches.models import Coach, Venue, Client, Session


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
    google_calander_url = models.URLField(null=True)


    @property
    def venue_name(self):
        return self.venue.name if self.venue else self.custome_venue

    @property
    def service_name(self):
        return self.service.name

    @property
    def client_name(self):
        return self.client.full_name

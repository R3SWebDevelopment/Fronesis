from django.db import models
from coaches.models import Coach, Venue, Client, Session


class Appointments(models.Model):
    coach = models.ForeignKey(Coach, null=False, related_name='appointments')
    starts_datetime = models.DateTimeField(null=True)
    ends_datetime = models.DateTimeField(null=True)
    venue = models.ForeignKey(Venue, null=True, related_name='appointments')
    client = models.ForeignKey(Client, null=False, related_name='appointments')
    service = models.ForeignKey(Session, null=True, related_name='appointments')

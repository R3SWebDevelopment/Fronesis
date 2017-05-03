from django.db import models
import uuid


# Create your models here.
class Event(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4(), editable=False, null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=150)
    description = models.TextField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)

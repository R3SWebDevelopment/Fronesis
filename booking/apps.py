from django.apps import AppConfig
from django.db.models.signals import post_save


class BookingConfig(AppConfig):
    name = 'booking'

    def ready(self):
        from canvas.models import Appointments
        from canvas.signals import (create_appointment)

        post_save.connect(create_appointment, sender=Appointments)

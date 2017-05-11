from django.test import TestCase
from .models import Event
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from django.conf import settings


def user_factory(first_name, last_name, email):
    user = User.objects.create_user(email=email, username=email, password=email)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user


class EventTestCase(TestCase):

    def setUp(self):

        event_arena_monterrey_image_path = '{}/{}'.format(settings.BASE_DIR, '.static/img/event-featured.png')

        self.event_arena_monterrey = Event()
        self.event_arena_monterrey.title = 'Python Con Mexico 2017'
        self.event_arena_monterrey.subtitle = 'Reunion anual python 2017'
        self.event_arena_monterrey.description = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. ' \
                                                 'Aenean commodo ligula eget dolor. Aenean massa. Cum sociis ' \
                                                 'natoque penatibus et magnis dis parturient montes, nascetur ' \
                                                 'ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu.'
        self.event_arena_monterrey.date = datetime.strptime('2017-02-18', '%Y-%B-%d').date()
        self.event_arena_monterrey.date = datetime.strptime('20:00', '%H:%M').time()
        self.event_arena_monterrey.duration = timedelta(hours=2)
        self.event_arena_monterrey.location = 'Monterrey, México'
        self.event_arena_monterrey.venue = 'Arena Monterrey'
        self.event_arena_monterrey.address = 'Avenida Francisco I. Madero 2500, Obrera, 64010 Monterrey, N.L.'
        self.event_arena_monterrey.cover = SimpleUploadedFile(name='test_image.jpg',
                                                              content=open(event_arena_monterrey_image_path,
                                                                           'rb').read(),
                                                              content_type='image/jpeg')
        self.event_arena_monterrey.organizer.add(user_factory('Ricardo', 'Tercero', 'ricardo.tercero@vordem.mx'))
        self.event_arena_monterrey.tickets_selling_begins_date = datetime.strptime('2017-02-01T00:00', '%Y-%B-%dT%H:%M')
        self.event_arena_monterrey.tickets_selling_ends_date = datetime.strptime('2017-02-18T20:00', '%Y-%B-%dT%H:%M')
        self.event_arena_monterrey.save()


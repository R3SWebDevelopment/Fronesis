from .views import DummyView, CreateEventView, MyEventsView, EventsPublished, EventView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', EventsPublished.as_view(), name='events'),
    url(r'^my_events/$', MyEventsView.as_view(), name='my_events'),
    url(r'^my_events/create/$', CreateEventView.as_view(), {'mode': 'create'}, name='my_events_create'),
    url(r'^my_events/(?P<event_uuid>[0-9A-Fa-f-]+)/edit/$', EventView.as_view(), {'mode': 'update'},
        name='my_events_update'),


    # Dummy views
    url(r'^index.html$', DummyView.as_view(), {'template_name': 'index.html'}),
    url(r'^list-events.html$', DummyView.as_view(), {'template_name': 'events/list-events.html',
                                                     'body_class': 'bg-white'}),
    url(r'^new-event.html$', DummyView.as_view(), {'template_name': 'events/new-event.html', 'body_class': 'bg-white'}),
    url(r'^all-events.html$', DummyView.as_view(), {'template_name': 'events/all-events.html',
                                                    'body_class': 'bg-white'}),
    url(r'^public-view-event.html$', DummyView.as_view(), {'template_name': 'events/public-view-event.html',
                                                           'body_class': 'bg-white'}),

    url(r'^booking.html$', DummyView.as_view(), {'template_name': 'booking.html', 'body_class': 'bg-white'}),
]


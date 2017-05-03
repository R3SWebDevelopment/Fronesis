from .views import DummyView
from django.conf.urls import url

urlpatterns = [
    url(r'^index.html$', DummyView.as_view(), {'template_name': 'index.html'}),
    url(r'^list-events.html$', DummyView.as_view(), {'template_name': 'events/list-events.html',
                                                     'body_class': 'bg-white'}),
    url(r'^new-event.html$', DummyView.as_view(), {'template_name': 'events/new-event.html', 'body_class': 'bg-white'}),
    url(r'^all-events.html$', DummyView.as_view(), {'template_name': 'events/all-events.html',
                                                    'body_class': 'bg-white'}),
    url(r'^public-view-event.html$', DummyView.as_view(), {'template_name': 'events/public-view-event.html', 'body_class': 'bg-white'}),

    url(r'^booking.html$', DummyView.as_view(), {'template_name': 'booking.html', 'body_class': 'bg-white'}),
]


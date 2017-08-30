from .views import DummyView, CreateEventView, MyEventsView, EventsPublished, EventView, EventDetailPublished, \
    EventGetTicket, EventGetTicketCheckOut, EventGetTicketCheckOutFinished, EventTicketSalesReport, MyTicketsListView
from django.conf.urls import url

from django.contrib.auth.decorators import permission_required

urlpatterns = [
    url(r'^$', EventsPublished.as_view(), name='events'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>\w+)/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)/(?P<event_uuid>[\w-]+)/$',
        EventDetailPublished.as_view(), name='public_event'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>\w+)/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)/(?P<event_uuid>[\w-]+)/get-tickets/$',
        EventGetTicket.as_view(), name='public_event_tickets'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>\w+)/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)/(?P<event_uuid>[\w-]+)/get-tickets/'
        r'checkout/$', EventGetTicketCheckOut.as_view(), name='public_event_tickets_checkout'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>\w+)/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)/(?P<event_uuid>[\w-]+)/get-tickets/'
        r'checkout/finish/$', EventGetTicketCheckOutFinished.as_view(), name='public_event_tickets_checkout_finish'),
    url(r'^my_events/$',
        permission_required('events.edit_event', login_url='/events/')(MyEventsView.as_view()), name='my_events'),
    url(r'^my_events/create/$',
        permission_required('events.create_event', login_url='/events/')(CreateEventView.as_view()),
        {'mode': 'create'}, name='my_events_create'),
    url(r'^my_events/(?P<event_uuid>[0-9A-Fa-f-]+)/edit/$',
        permission_required('events.create_event',
                            login_url='/events/')(EventView.as_view()), {'mode': 'update'}, name='my_events_update'),
    url(r'^my_events/(?P<event_uuid>[0-9A-Fa-f-]+)/tickets_sales_report/$',
        permission_required('events.edit_event', login_url='/events/')(EventTicketSalesReport.as_view()),
        name='my_events_tickets_sales_report'),
    url(r'^my_tickets/$', MyTicketsListView.as_view(), name='MyTicketsListView'),


    # Dummy views
    # url(r'^index.html$', DummyView.as_view(), {'template_name': 'index.html'}),
    # url(r'^list-events.html$', DummyView.as_view(), {'template_name': 'events/list-events.html',
    #                                                  'body_class': 'bg-white'}),
    # url(r'^new-event.html$', DummyView.as_view(), {'template_name': 'events/new-event.html', 'body_class': 'bg-white'}),
    # url(r'^all-events.html$', DummyView.as_view(), {'template_name': 'events/all-events.html',
    #                                                 'body_class': 'bg-white'}),
    # url(r'^public-view-event.html$', DummyView.as_view(), {'template_name': 'events/public-view-event.html',
    #                                                        'body_class': 'bg-white'}),
    #
    # url(r'^booking.html$', DummyView.as_view(), {'template_name': 'booking.html', 'body_class': 'bg-white'}),
]


from .views import ContactDetail, BlockedHours, BookingSettings, MyVenues, CreateVenues, RemoveVenues, EditVenues, \
    MyServices, CreateService, EditService
from django.conf.urls import url

urlpatterns = [
    url(r'^contact_information/$', ContactDetail.as_view(), name='contact_information'),
    url(r'^blocked_hours/$', BlockedHours.as_view(), name='blocked_hours'),
    url(r'^booking_settings/$', BookingSettings.as_view(), name='booking_settings'),
    url(r'^my_venues/$', MyVenues.as_view(), name='my_venues'),
    url(r'^my_venues/add/$', CreateVenues.as_view(), name='add_venues'),
    url(r'^my_venues/(?P<pk>\d+)/remove/$', RemoveVenues.as_view(), name='remove_venues'),
    url(r'^my_venues/(?P<pk>\d+)/edit/$', EditVenues.as_view(), name='edit_venues'),
    url(r'^my_services/$', MyServices.as_view(), name='my_services'),
    url(r'^my_services/add/$', CreateService.as_view(), name='add_services'),
    url(r'^my_services/(?P<pk>\d+)/edit/$', EditService.as_view(), name='edit_services'),
]


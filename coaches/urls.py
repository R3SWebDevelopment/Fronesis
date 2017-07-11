from .views import ContactDetail, BlockedHours, BookingSettings, MyVenues
from django.conf.urls import url

urlpatterns = [
    url(r'^contact_information/$', ContactDetail.as_view(), name='contact_information'),
    url(r'^blocked_hours/$', BlockedHours.as_view(), name='blocked_hours'),
    url(r'^booking_settings/$', BookingSettings.as_view(), name='booking_settings'),
    url(r'^my_venues/$', MyVenues.as_view(), name='my_venues'),


]


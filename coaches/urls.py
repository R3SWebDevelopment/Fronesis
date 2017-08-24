from .views import ContactDetail, BlockedHours, BookingSettings, MyVenues, CreateVenues, RemoveVenues, EditVenues, \
    MyServices, CreateService, EditService, CommunityView, CoachDetailView, CreateBundle, EditBundle
from django.conf.urls import url

from django.contrib.auth.decorators import permission_required

urlpatterns = [
    url(r'^(?P<pk>\d+)/detail/$', CoachDetailView.as_view(), name='detail'),
    url(r'^community/$', CommunityView.as_view(), name='community'),
    url(r'^contact_information/$', permission_required('coaches.edit_contact_info')(ContactDetail.as_view()),
        name='contact_information'),
    url(r'^blocked_hours/$', permission_required('coaches.edit_blocked_hours')(BlockedHours.as_view()),
        name='blocked_hours'),
    url(r'^booking_settings/$', permission_required('coaches.edit_booking_settings')(BookingSettings.as_view()),
        name='booking_settings'),
    url(r'^my_venues/$', permission_required('coaches.edit_venues')(MyVenues.as_view()), name='my_venues'),
    url(r'^my_venues/add/$', permission_required('coaches.edit_venues')(CreateVenues.as_view()), name='add_venues'),
    url(r'^my_venues/(?P<pk>\d+)/remove/$', permission_required('coaches.edit_venues')(RemoveVenues.as_view()),
        name='remove_venues'),
    url(r'^my_venues/(?P<pk>\d+)/edit/$', permission_required('coaches.edit_venues')(EditVenues.as_view()),
        name='edit_venues'),
    url(r'^my_services/$', permission_required('coaches.edit_my_services')(MyServices.as_view()), name='my_services'),
    url(r'^my_services/add/$', permission_required('coaches.edit_my_services')(CreateService.as_view()),
        name='add_services'),
    url(r'^my_services/(?P<pk>\d+)/edit/$', permission_required('coaches.edit_my_services')(EditService.as_view()),
        name='edit_services'),
    url(r'^my_bundles/add/$', permission_required('coaches.edit_bundle')(CreateBundle.as_view()), name='add_bundles'),
    url(r'^my_bundles/(?P<pk>\d+)/edit/$$', permission_required('coaches.edit_bundle')(EditBundle.as_view()),
        name='edit_bundles'),
]


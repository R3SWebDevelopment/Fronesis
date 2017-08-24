from .views import CalendarView, HistoryView, ClientsView, BundleView, AddAppointmentView, AppointmentRequestView, \
    AppointmentRequestRemoveView, AppointmentRequestConfirmView, AppointmentClientSideModalView
from django.conf.urls import url

from django.contrib.auth.decorators import permission_required

urlpatterns = [
    url(r'^calendar_view/$', permission_required('booking.view_coach_appointment')(CalendarView.as_view()),
        name='calendar_view'),
    url(r'^history/$', permission_required('booking.appointment_history')(HistoryView.as_view()), name='history'),
    url(r'^clients/$', permission_required('booking.view_clients')(ClientsView.as_view()), name='clients'),
    url(r'^bundles/$', permission_required('booking.view_active_bundles')(BundleView.as_view()), name='bundles'),
    url(r'^add/$', permission_required('booking.add_appointment_coach_side')(AddAppointmentView.as_view()), name='add_appointment'),
    url(r'^confirmation/$', permission_required('booking.confirm_appointment')(AppointmentRequestView.as_view()),
        name='confirmation'),
    url(r'^confirmation/(?P<pk>\d+)/remove/$',
        permission_required('booking.confirm_appointment')(AppointmentRequestRemoveView.as_view()),
        name='confirmation_remove'),
    url(r'^confirmation/(?P<pk>\d+)/confirm/$',
        permission_required('booking.confirm_appointment')(AppointmentRequestConfirmView.as_view()),
        name='confirmation_confirm'),
    url(r'^client-side/(?P<pk>\d+)/modal/$', AppointmentClientSideModalView.as_view(), name='client_side_modal'),
]


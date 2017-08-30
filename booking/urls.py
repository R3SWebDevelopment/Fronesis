from .views import CalendarView, HistoryView, ClientsView, BundleView, AddAppointmentView, AppointmentRequestView, \
    AppointmentRequestRemoveView, AppointmentRequestConfirmView, AppointmentClientSideModalView, MyAppointmentsView,\
    PayAppointmentView, PayAppointmentByCreditCardView, PayAppointmentByCreditCardNotificationView
from django.conf.urls import url

from django.contrib.auth.decorators import permission_required

urlpatterns = [
    url(r'^calendar_view/$', permission_required('booking.view_coach_appointment',
                                                 login_url='/booking/my_appointments/')(CalendarView.as_view()),
        name='calendar_view'),
    url(r'^my_appointments/$', MyAppointmentsView.as_view(), name='my_appointments'),
    url(r'^history/$',
        permission_required('booking.appointment_history',
                            login_url='/booking/my_appointments/')(HistoryView.as_view()), name='history'),
    url(r'^clients/$',
        permission_required('booking.view_clients',
                            login_url='/booking/my_appointments/')(ClientsView.as_view()), name='clients'),
    url(r'^bundles/$', permission_required('booking.view_active_bundles', login_url='/booking/my_appointments/')
    (BundleView.as_view()), name='bundles'),
    url(r'^add/$',
        permission_required('booking.add_appointment_coach_side',
                            login_url='/booking/my_appointments/')(AddAppointmentView.as_view()),
        name='add_appointment'),
    url(r'^pay_appointment/(?P<pk>\d+)/$', PayAppointmentView.as_view(), name='pay_appointment'),
    url(r'^pay_appointment/(?P<pk>\d+)/credit_card/$', PayAppointmentByCreditCardView.as_view(),
        name='pay_appointment_by_cc'),
    url(r'^pay_appointment/(?P<pk>\d+)/credit_card/notification/$',
        PayAppointmentByCreditCardNotificationView.as_view(), name='pay_appointment_by_cc_notification'),
    url(r'^confirmation/$',
        permission_required('booking.confirm_appointment',
                            login_url='/booking/my_appointments/')(AppointmentRequestView.as_view()),
        name='confirmation'),
    url(r'^confirmation/(?P<pk>\d+)/remove/$',
        permission_required('booking.confirm_appointment', login_url='/booking/my_appointments/')
        (AppointmentRequestRemoveView.as_view()),
        name='confirmation_remove'),
    url(r'^confirmation/(?P<pk>\d+)/confirm/$',
        permission_required('booking.confirm_appointment', login_url='/booking/my_appointments/')
        (AppointmentRequestConfirmView.as_view()),
        name='confirmation_confirm'),
    url(r'^client-side/(?P<pk>\d+)/modal/$', AppointmentClientSideModalView.as_view(), name='client_side_modal'),
]


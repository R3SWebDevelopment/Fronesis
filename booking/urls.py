from .views import CalendarView, HistoryView, ClientsView, BundleView, AddAppointmentView, AppointmentRequestView
from django.conf.urls import url

urlpatterns = [
    url(r'^calendar_view/$', CalendarView.as_view(), name='calendar_view'),
    url(r'^history/$', HistoryView.as_view(), name='history'),
    url(r'^clients/$', ClientsView.as_view(), name='clients'),
    url(r'^bundles/$', BundleView.as_view(), name='bundles'),
    url(r'^add/$', AddAppointmentView.as_view(), name='add_appointment'),
    url(r'^confirmation/$', AppointmentRequestView.as_view(), name='confirmation'),
]


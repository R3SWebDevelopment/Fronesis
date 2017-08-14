# from .views import auth_return, auth_return_appointment, connect_calender, disconnect_calender, add_appointment
from .views import connect_calender, auth_return, disconnect_calender
from django.conf.urls import url

urlpatterns = [
    url(r'^calendar/connect/$', connect_calender, name='calendar_connect'),
    url(r'^oauth2callback/$', auth_return, name='auth_return'),
    url(r'^calendar/disconnect/$', disconnect_calender, name='calendar_disconnect'),
    # url(r'^oauth2callback/$', auth_return, name='auth_return'),
    # url(r'^oauth2callback/appointment/$', auth_return_appointment, name='auth_return_appointment'),
    # url(r'^calendar/connect/$', connect_calender, name='calendar_connect'),
    # url(r'^calendar/disconnect/$', disconnect_calender, name='calendar_disconnect'),
    # url(r'^calendar/appointment/(?P<pk>\d+)/add/$', add_appointment, name='add_appointment'),
]


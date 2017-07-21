from .views import auth_return, connect_calender
from django.conf.urls import url

urlpatterns = [
    url(r'^oauth2callback/$', auth_return, name='auth_return'),
    url(r'^calendar/connect/$', connect_calender, name='calendar_connect'),
]


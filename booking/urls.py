from .views import CalendarView
from django.conf.urls import url

urlpatterns = [
    url(r'^calendar_view/$', CalendarView.as_view(), name='calendar_view'),
]


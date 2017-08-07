from rest_framework import viewsets
from .serializers import Coach, Appointments
from .serializers import AvailableTimeSerializer, AppointmentsSerializer, PreviewAppointmentsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route
from datetime import datetime
from datetime import timedelta


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = AvailableTimeSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super(CalendarViewSet, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).first()


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentsSerializer

    is_preview = False

    def get_queryset(self, *args, **kwargs):
        qs = super(AppointmentViewSet, self).get_queryset(*args, **kwargs)
        user = self.request.user
        coach = user.coaches.first()
        return qs.filter(coach=coach)

    @detail_route(methods=['get'], url_path='preview')
    def preview(self, request, *args, **kwargs):
        user = self.request.user
        coach = user.coaches.first()
        session = None
        client_id = self.request.query_params.get('client_id', None)
        session_id = self.request.query_params.get('session_id', None)
        date = self.request.query_params.get('date', None)
        hour = self.request.query_params.get('hour', None)
        venue_id = self.request.query_params.get('venue_id', None)
        date_time_available = False
        response_data = {}
        if client_id:
            client = coach.clients.filter(pk=client_id).first()
            if client:
                response_data.update({
                    'client_name': client.full_name
                })
        if session_id:
            session = coach.services.filter(pk=session_id).first()
            if session:
                response_data.update({
                    'session_name': session.name
                })
        if venue_id:
            venues = session.allow_on_venues.all() if session else coach.venues.all()
            venue = venues.filter(pk=venue_id).first()
            if venue:
                response_data.update({
                    'venue_name': venue.name
                })
        if date and hour:
            valid_date = False
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
                valid_date = True
            except:
                pass
            if valid_date:
                weekday = date.isoweekday()
                hours = coach.available_hours.filter(day=weekday)
                hour = hours.filter(pk=hour).first()
                if hour:
                    begins_datetime = date.replace(hour=hour.hour)
                    if session:
                        length_hours = session.length_hours or 0
                        length_minutes = session.length_minutes or 0
                        session_delta = timedelta(minutes=length_minutes, hours=length_hours)
                        ends_datetime = begins_datetime + session_delta
                        appointments = coach.appointments.exclude(starts_datetime__gte=ends_datetime).\
                            exclude(ends_datetime__lte=begins_datetime)
                        if not appointments.exists():
                            date_time_available = True
                            session_time = '{} - {}'.format(begins_datetime.strftime('%I:%M %p'),
                                                            ends_datetime.strftime('%I:%M %p'))
                            session_date = begins_datetime.strftime('%A, %d/%b/%Y')
                            response_data.update({
                                'session_time': session_time,
                                'session_date': session_date,
                            })
                    else:
                        ends_datetime = None
        response_data.update({
            'date_time_available': date_time_available
        })
        serialized = PreviewAppointmentsSerializer(data=response_data)
        serialized.is_valid()
        return Response(serialized.data)

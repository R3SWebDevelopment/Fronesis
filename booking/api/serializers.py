from rest_framework import serializers
from ..models import Appointments, Coach
from coaches.models import AvailableHour
from coaches.api.serializers import VenueSerializer, ClientSerializer, SessionSerializer
from datetime import datetime
from crum import get_current_user
from rest_framework import status
from datetime import datetime
from datetime import time
from datetime import timedelta


class AppointmentsSerializer(serializers.ModelSerializer):
    starts_datetime = serializers.DateTimeField(read_only=True)
    ends_datetime = serializers.DateTimeField(read_only=True)
    custome_venue = serializers.CharField(required=False, allow_blank=True)
    online_call = serializers.BooleanField(required=False, default=False)
    venue = VenueSerializer(read_only=True)
    venue_id = serializers.IntegerField(write_only=True, required=False)
    client = ClientSerializer(read_only=True)
    client_id = serializers.IntegerField(write_only=True, required=True)
    service = SessionSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True, format='%Y-%m-%d')
    time = serializers.IntegerField(write_only=True, required=True)
    already_paid = serializers.BooleanField(write_only=True, default=False)
    send_payment_link = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = Appointments
        fields = ('id', 'starts_datetime', 'ends_datetime', 'custome_venue', 'online_call', 'venue', 'venue_id', 'client',
                  'client_id', 'service', 'service_id', 'date', 'time', 'already_paid', 'send_payment_link')

    def create(self, validated_data):
        current_user = get_current_user()
        coach = current_user.coaches.first()
        instance = None
        client = None
        session = None
        begins_datetime = None
        ends_datetime = None
        venue = None
        custome_venue = validated_data.get('custome_venue', None)
        online_call = validated_data.get('online_call', False)
        already_paid = validated_data.get('already_paid', False)
        send_payment_link = validated_data.get('send_payment_link', False)
        if coach:
            client_id = validated_data.get('client_id', None)
            if client_id:
                client = coach.clients.filter(pk=client_id).first()
            if client is None:
                raise serializers.ValidationError('This is not your client', code=status.HTTP_400_BAD_REQUEST)
            session_id = validated_data.get('service_id', None)
            if session_id:
                session = coach.services.filter(pk=session_id).first()
            if session is None:
                raise serializers.ValidationError('You are not giving this service', code=status.HTTP_400_BAD_REQUEST)
            date = validated_data.get('date', None)
            hour = validated_data.get('time', None)
            if date and hour:
                if date:
                    date = datetime.combine(date, datetime.min.time())
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
                            appointments = coach.appointments.exclude(starts_datetime__gte=ends_datetime). \
                                exclude(ends_datetime__lte=begins_datetime)
                            if appointments.exists():
                                raise serializers.ValidationError('You already have an appointment at this this',
                                                                  code=status.HTTP_400_BAD_REQUEST)
                        else:
                            ends_datetime = None
                    else:
                        raise serializers.ValidationError("You don't have this time available",
                                                          code=status.HTTP_400_BAD_REQUEST)
            if begins_datetime is None and ends_datetime is None:
                raise serializers.ValidationError('The time you select for this appointment is not correct',
                                                  code=status.HTTP_400_BAD_REQUEST)
            venue_id = validated_data.get('venue_id', None)
            if venue_id:
                venues = session.allow_on_venues.all() if session else coach.venues.all()
                venues = coach.venues.all()
                venue = venues.filter(pk=venue_id).first()
            if venue is None and custome_venue is None:
                raise serializers.ValidationError('You can use the venue you select', code=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError('No coach instance', code=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Appointments.objects.create(coach=coach, starts_datetime=begins_datetime,
                                                   ends_datetime=ends_datetime, online_call=online_call,
                                                   custome_venue=custome_venue, venue=venue, client=client,
                                                   service=session, already_paid=already_paid,
                                                   send_payment_link=send_payment_link)
        except:
            raise serializers.ValidationError('There was an error while adding the appointment',
                                              code=status.HTTP_400_BAD_REQUEST)
        return instance


class PreviewAppointmentsSerializer(serializers.Serializer):
    session_name = serializers.CharField(max_length=200)
    session_time = serializers.CharField(max_length=200)
    session_date = serializers.CharField(max_length=200)
    session_price = serializers.CharField(max_length=200)
    client_name = serializers.CharField(max_length=200)
    venue_name = serializers.CharField(max_length=200)
    date_time_available = serializers.BooleanField()


class AvailableHourSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AvailableHour
        fields = ('time', 'id')

    def get_time(self, obj):
        return "0{}:00".format(obj.hour) if obj.hour < 10 else "{}:00".format(obj.hour)


class AvailableTimeSerializer(serializers.ModelSerializer):
    appointments = serializers.SerializerMethodField(read_only=True)
    date_times = serializers.SerializerMethodField(read_only=True)
    small_date = serializers.SerializerMethodField(read_only=True)
    min_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Coach
        fields = ('appointments', 'date_times', 'small_date', 'min_date')

    def get_min_date(self, obj, *args, **kwargs):
        context = self.context
        date = datetime.now().date()
        return date.strftime('%Y-%m-%d')


    def get_small_date(self, obj, *args, **kwargs):
        context = self.context
        date = datetime.now().date()
        if context:
            request = context.get('request', None)
            if request:
                query_date = request.query_params.get('date', None)
                try:
                    query_date = datetime.strptime(query_date, '%Y-%m-%d').date()
                    date = query_date if date < query_date else date
                except:
                    pass
        return date.strftime('%b %d')

    def get_appointments(self, obj, *args, **kwargs):
        context = self.context
        date = datetime.now().date()
        if context:
            request = context.get('request', None)
            if request:
                query_date = request.query_params.get('date', None)
                try:
                    query_date = datetime.strptime(query_date, '%Y-%m-%d').date()
                    date = query_date if date < query_date else date
                except:
                    pass
        appointments = obj.appointments.all()
        appointments = appointments.filter(starts_datetime__range=(datetime.combine(date, time.min),
                                                                   datetime.combine(date, time.max)))
        return AppointmentsSerializer(appointments, many=True).data

    def get_date_times(self, obj, *args, **kwargs):
        context = self.context
        date = datetime.now().date()
        if context:
            request = context.get('request', None)
            if request:
                query_date = request.query_params.get('date', None)
                try:
                    query_date = datetime.strptime(query_date, '%Y-%m-%d').date()
                    date = query_date if date < query_date else date
                except:
                    pass
        weekday = date.isoweekday()
        available = obj.available_hours.filter(day=weekday)
        return AvailableHourSerializer(available, many=True).data

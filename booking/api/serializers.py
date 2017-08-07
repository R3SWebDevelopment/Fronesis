from rest_framework import serializers
from ..models import Appointments, Coach
from coaches.models import AvailableHour
from coaches.api.serializers import VenueSerializer, ClientSerializer, SessionSerializer
from datetime import datetime


class AppointmentsSerializer(serializers.ModelSerializer):
    starts_datetime = serializers.DateTimeField(read_only=True)
    ends_datetime = serializers.DateTimeField(read_only=True)
    custome_venue = serializers.CharField(required=False)
    online_call = serializers.BooleanField(required=False, default=False)
    venue = VenueSerializer(read_only=True)
    venue_id = serializers.IntegerField(write_only=True, required=False)
    client = ClientSerializer(read_only=True)
    client_id = serializers.IntegerField(write_only=True, required=True)
    service = SessionSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True, required=True)
    date = serializers.DateField(write_only=True, required=True, input_formats='%Y-%m-%d')
    time = serializers.IntegerField(write_only=True, required=True)
    already_paid = serializers.BooleanField(write_only=True, default=False)
    send_payment_link = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = Appointments
        fields = ('starts_datetime', 'ends_datetime', 'custome_venue', 'online_call', 'venue', 'venue_id', 'client',
                  'client_id', 'service', 'service_id', 'date', 'time', 'already_paid', 'send_payment_link')


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

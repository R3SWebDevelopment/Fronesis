from rest_framework import serializers
from ..models import Appointments, Coach
from coaches.models import AvailableHour
from datetime import datetime


class AppointmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointments
        fields = '__all__'


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
                    query_date = datetime.strptime(query_date, '%d/%m/%Y').date()
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
                    query_date = datetime.strptime(query_date, '%d/%m/%Y').date()
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
                    query_date = datetime.strptime(query_date, '%d/%m/%Y').date()
                    date = query_date if date < query_date else date
                except:
                    pass
        weekday = date.isoweekday()
        available = obj.available_hours.filter(day=weekday)
        return AvailableHourSerializer(available, many=True).data

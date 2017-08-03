from rest_framework import serializers
from ..models import Client, Session, Venue
from crum import get_current_user


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'full_name', 'email')

    def create(self, validated_data):
        instance = super(ClientSerializer, self).create(validated_data)
        current_user = get_current_user()
        if current_user:
            coach = current_user.coaches.first()
            if coach:
                coach.clients.add(instance)
        return instance


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('id', 'name', 'address')


class SessionSerializer(serializers.ModelSerializer):
    length = serializers.SerializerMethodField(read_only=True)
    allow_on_venues = VenueSerializer(many=True)

    class Meta:
        model = Session
        fields = ('id', 'name', 'price', 'allow_on_venues', 'length')

    def get_length(self, obj):
        context, duration = "hour", "00:00"
        if obj.length_hours and obj.length_minutes:
            duration = "{}:{}".format(
                "0{}".format(obj.length_hours) if obj.length_hours < 10 else "{}".format(obj.length_hours),
                "0{}".format(obj.length_minutes) if obj.length_minutes < 10 else "{}".format(obj.length_minutes)
            )
            context = 'hours' if obj.length_hours > 1 else 'hour'
        elif obj.length_hours:
            duration = "{}".format(
                "{}".format(obj.length_hours)
            )
            context = 'hours' if obj.length_hours > 1 else 'hour'
        elif obj.length_minutes:
            duration = "{}".format(
                "{}".format(obj.length_minutes)
            )
            context = 'minutes' if obj.length_minutes > 1 else 'minute'

        return "{} {}".format(duration, context)

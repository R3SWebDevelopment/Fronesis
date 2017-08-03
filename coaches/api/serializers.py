from rest_framework import serializers
from ..models import Client
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

from rest_framework import serializers
from drum.links.models import Link
from fronesis.users.serializers import UserSerializer
from mezzanine.generic.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Link
        fields = ['id', 'title', 'link', 'publish_date', 'user']
        read_only_fields = ['publish_date']

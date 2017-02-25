from rest_framework import serializers
from drum.links.models import Link
from fronesis.users.serializers import UserSerializer
from mezzanine.generic.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'value', 'object_pk']


class LinkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Link
        fields = [
            'id', 'title', 'link', 'publish_date',
            'rating_sum', 'user'
        ]
        read_only_fields = ['publish_date']

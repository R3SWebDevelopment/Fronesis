from rest_framework import serializers
from drum.links.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'user', 'title', 'link', 'publish_date',)
        read_only_fields = ('publish_date',)
        depth = 1

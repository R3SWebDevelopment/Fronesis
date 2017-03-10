from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer
from mezzanine.generic.models import Rating
from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'value', 'object_pk']
        read_only_fields = ['id']


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'link', 'description', 'tags',
            'publish_date', 'rating_sum', 'user'
        ]
        read_only_fields = ['publish_date']

from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer
from mezzanine.generic.models import Rating
from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'value', 'object_pk']
        filter_fields = ('user', 'object_pk',)
        read_only_fields = ['id']


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_rating = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'link', 'description', 'tags',
            'publish_date', 'rating_sum', 'user', 'user_rating',
        ]
        read_only_fields = ['publish_date']

    def get_user_rating(self, obj):
        rating = obj.rating.filter(user=self.context['request'].user)

        return RatingSerializer(
            rating.first(), many=False
        ).data if rating.exists() else None

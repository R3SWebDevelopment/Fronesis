from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from users.serializers import UserSerializer
from mezzanine.generic.models import Rating
from django_comments.models import Comment
from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)
from django.conf import settings
from .models import Post


def get_post_content_type():
    return ContentType.objects.get_for_model(Post)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'value', 'object_pk']
        filter_fields = ('user', 'object_pk',)
        read_only_fields = ['id', 'user']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'object_pk', 'comment', 'submit_date']
        filter_fields = ['user', 'object_pk']
        read_only_fields = ('user', 'submit_date')


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_rating = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'link', 'description', 'tags',
            'publish_date', 'rating_sum', 'user', 'user_rating',
            'comments_count'
        ]
        read_only_fields = ['user', 'user_rating', 'publish_date']

    def get_user_rating(self, obj):
        rating = obj.rating.filter(user=self.context['request'].user)

        return RatingSerializer(
            rating.first(), many=False
        ).data if rating.exists() else None

    def get_comments_count(self, obj):
        return self._get_comments(obj).count() or 0

    def _get_comments(self, obj):
        return Comment.objects.filter(
            object_pk=obj.pk,
            content_type=get_post_content_type(),
            is_removed=False,
            site_id=settings.SITE_ID
        )

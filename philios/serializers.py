from django.contrib.contenttypes.models import ContentType
from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_framework import serializers
from utils.urls import (
    split_url, valid_url_mimetype
)
from django.utils.translation import ugettext as _
from users.serializers import UserSerializer
from mezzanine.generic.models import Rating
from django_comments.models import Comment
from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)
from django.conf import settings
from .models import Post


def get_post_content_type():
    return ContentType.objects.get_for_model(Post)


def _invalidate(msg):
    raise serializers.ValidationError(_(msg))


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
    # image = VersatileImageFieldSerializer(
    #     required=False, sizes='post_image')
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'link', 'link_type', 'description', 'tags',
            'publish_date', 'rating_sum', 'user', 'user_rating',
            'comments_count', 'image'
        ]
        read_only_fields = ['user', 'user_rating', 'publish_date', 'image']

    def get_image(self, obj):
        if obj.image:
            return{
                'full_size': obj.image.url,
                'medium_square_crop': obj.image.crop['280x280'].url,
                'small_square_crop': obj.image.crop['50x50'].url,
                'thumbnail': obj.image.crop['280x280'].url,
            }
        else:
            beingIndex = obj.link.index("v=")
            parameters = obj.link[beingIndex + 2:]
            endIndex = parameters.index("&") if "&" in parameters else len(parameters)
            video_id = parameters[:endIndex]
            return{
                'full_size': 'http://img.youtube.com/vi/{}/maxresdefault.jpg'.format(video_id),
                'medium_square_crop': 'http://img.youtube.com/vi/{}/hqdefault.jpg'.format(video_id),
                'small_square_crop': 'http://img.youtube.com/vi/{}/mqdefault.jpg'.format(video_id),
                'thumbnail': 'http://img.youtube.com/vi/{}/1.jpg'.format(video_id),
            }

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

    def validate_tags(self, data):
        def _remove_spaces(str):
            return "".join(str.split())

        return [
            '#{}'.format(_remove_spaces(t))
            if not t.startswith('#')
            else _remove_spaces(t) for t in data]

    def _validate_image_link(self, value):
        url = value.lower()
        domain, path = split_url(url)

        # validate url first, image download will be done on the view
        if not valid_url_mimetype(url):
            _invalidate('Not a valid Image.')

    def _validate_video_link(self, value):
        pass

    def _validate_regular_link(self, value):
        pass

    def _validate_link(self, data):
        # set link validation depending on link type
        t = data['link_type']
        v = self._validate_image_link if t == Post.IMAGE \
            else self._validate_video_link if t == Post.VIDEO \
            else self._validate_regular_link

        v(data['link'])  # do the validation

    def validate(self, data):
        if 'image' not in data:  # if image wasnt uploaded
            self._validate_link(data)

        return data

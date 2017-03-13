from .serializers import (
    PostSerializer, RatingSerializer, CommentSerializer,
    get_post_content_type
)
from utils.mixins import OnlyAlterOwnObjectsViewSet
from mezzanine.generic.models import Rating
from django_comments.models import Comment
from django.conf import settings
from rest_framework import viewsets
from django.db import transaction
from .models import Post


class PostViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )


class CommentViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = CommentSerializer
    filter_fields = CommentSerializer.Meta.filter_fields
    queryset = Comment.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Comment.objects.filter(
            content_type=get_post_content_type()
        )

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user,
            content_type=get_post_content_type(),
            is_removed=False,
            site_id=settings.SITE_ID
        )


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    filter_fields = RatingSerializer.Meta.filter_fields
    queryset = Rating.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Rating.objects.filter(
            content_type=get_post_content_type()
        )

    def perform_create(self, serializer):
        with transaction.atomic():
            # TODO: move this to signals
            # delete previous ratings from the same user to the same object
            rating = serializer.validated_data
            Rating.objects.filter(
                user=self.request.user,
                content_type=get_post_content_type(),
                object_pk=rating['object_pk']
            ).delete()

            return serializer.save(
                user=self.request.user,
                content_type=get_post_content_type()
            )

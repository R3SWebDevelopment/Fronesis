from django.contrib.contenttypes.models import ContentType
from .serializers import PostSerializer, RatingSerializer
from utils.mixins import OnlyAlterOwnObjectsViewSet
from mezzanine.generic.models import Rating
from rest_framework import viewsets
from django.db import transaction
from .models import Post


def get_rating_content_type():
    return ContentType.objects.get_for_model(Post)


class PostViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def get_queryset(self):
        return Rating.objects.filter(
            content_type=get_rating_content_type()
        )

    def perform_create(self, serializer):
        with transaction.atomic():
            # delete previous ratings from the same user to the same object
            rating = serializer.validated_data
            Rating.objects.filter(
                user=self.request.user,
                content_type=get_rating_content_type(),
                object_pk=rating['object_pk']
            ).delete()

            return serializer.save(
                user=self.request.user,
                content_type=get_rating_content_type()
            )

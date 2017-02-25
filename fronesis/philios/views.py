from fronesis.utils.mixins import OnlyAlterOwnObjectsViewSet
from django.contrib.contenttypes.models import ContentType
from .serializers import LinkSerializer, RatingSerializer
from mezzanine.generic.models import Rating
from drum.links.models import Link
from rest_framework import viewsets
from django.db import transaction


rating_content_type = ContentType.objects.get_for_model(Link)


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.filter(
        content_type=rating_content_type
    )

    def perform_create(self, serializer):
        with transaction.atomic():
            # delete previous ratings from the same user to the same object
            rating = self.get_object()
            Rating.objects.filter(
                user=self.request.user,
                content_type=rating_content_type,
                object_pk=rating.object_pk
            ).delete()

            return serializer.save(
                user=self.request.user,
                content_type=rating_content_type
            )


class LinkViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )

from fronesis.utils.mixins import OnlyAlterOwnObjectsViewSet
from django.contrib.contenttypes.models import ContentType
from .serializers import LinkSerializer, RatingSerializer
from mezzanine.generic.models import Rating
from drum.links.models import Link
from rest_framework import viewsets


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.filter(
        content_type=ContentType.objects.get_for_model(Link)
    )


class LinkViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )

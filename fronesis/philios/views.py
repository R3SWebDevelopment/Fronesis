from fronesis.utils.mixins import OnlyAlterOwnObjectsViewSet
from .serializers import LinkSerializer
from drum.links.models import Link


class LinkViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )

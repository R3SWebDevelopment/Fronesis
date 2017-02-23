from rest_framework import viewsets
from .serializers import LinkSerializer
from drum.links.models import Link


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )
